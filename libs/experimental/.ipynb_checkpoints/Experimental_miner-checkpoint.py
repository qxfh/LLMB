import importlib
import json
import copy
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from .prompt import * 

class All_ExperimentalMiner:
    def __init__(self, experimental_texts, original_summary, openai_api_key=None):
        
        self.experimental_texts = experimental_texts
        self.original_summary = original_summary
        self.openai_api_key = openai_api_key
        self.get_major_categories()

        if not self.material and not self.measurement:
            return

        self.sub_categories = self.get_sub_categories()
        self.sub_measurement = self.get_sub_measurement()
        self.sub_ = self.get_sub_()
        self.experimental_text_dict = self.get_experimental_text_dict()
        self.sub_categories_dict = self.get_sub_categories_dict()
        self.cell_summary = self.update_summary()
        self.material_dictionary = self.get_material_dictionary()
        self.summary_dict = self.get_summary_dict()
        
    def get_major_categories(self):
        major_categories = []
        material, synthesis, measurement = [], [], [] 
        prompt = PromptTemplate.from_template(PROMPT_MAJOR_CATEGORIZE)
        llm_major = ChatOpenAI(temperature=0.0, model_name='gpt-4', openai_api_key=self.openai_api_key)
        for index, text in enumerate(self.experimental_texts):
            output = llm_major.predict(prompt.format(paragraph=text))
            categories = json.loads(output)
            major_categories.append([index, categories])
            if 'material' in categories:
                material.append(index) 
            if 'synthesis' in categories:
                synthesis.append(index)
            if 'measurement' in categories:
                measurement.append(index)
                
        self.major_categories = major_categories
        self.material = material
        self.synthesis = synthesis
        self.measurement = measurement
        return           

    def get_sub_categories(self):
        sub_categories = []        
        prompt = PromptTemplate.from_template(PROMPT_SUB_CATEGORIZE)
        llm_sub = ChatOpenAI(temperature=0.0, model_name='gpt-4', openai_api_key=self.openai_api_key)
        for index in self.material:
            output = llm_sub.predict(prompt.format(paragraph=self.experimental_texts[index]))
            if isinstance(output, str):
                output = json.loads(output)
            sub_categories.append([index, output])
        return sub_categories

    def get_sub_measurement(self):
        sub_measurement = []
        prompt_measurement = PromptTemplate.from_template(PROMPT_SUB_MEASUREMENT)
        llm_sub = ChatOpenAI(temperature=0.0, model_name='gpt-4', openai_api_key=self.openai_api_key)
        for index in self.measurement:
            output = llm_sub.predict(prompt_measurement.format(paragraph=self.experimental_texts[index]))
            if isinstance(output, str):
                output = json.loads(output)
            sub_measurement.append([index, output])
        return sub_measurement
    
    def get_sub_(self):
        sub_categories_dict = dict(self.sub_categories)
        sub_measurement_dict = dict(self.sub_measurement)
        sub_ = []
        for key in sub_categories_dict:
            if key in sub_measurement_dict:
                combined_list = sub_categories_dict[key] + sub_measurement_dict[key]
                sub_.append([key, combined_list])
            else:
                sub_.append([key, sub_categories_dict[key]])

        for key in sub_measurement_dict:
            if not key in sub_categories_dict:
                sub_.append([key, sub_measurement_dict[key]])
        return sub_
    
    def get_experimental_text_dict(self):
        experimental_text_dict = {}
        for experimental_text in self.experimental_texts:
            experimental_text_dict[experimental_text] = ["else"] 
        for index, categories in self.sub_:
            experimental_text_dict[self.experimental_texts[index]] = categories
        return experimental_text_dict
    
    def get_sub_categories_dict(self):
        sub_categories_dict = {"cathode":[], "electrolyte":[], "anode":[], "separator":[], "current_collector":[], "cycle_performance":[], "EIS":[]}
        
        for index, categories in self.sub_:
            for category in categories:
                if category != "else":
                    sub_categories_dict[category].append(str(self.experimental_texts[index]))
                
        for category, texts in sub_categories_dict.items():
            combined_texts = ' '.join(texts)
            sub_categories_dict[category] = combined_texts
        return sub_categories_dict

    def preprocess_original_summary(self):
        sorted_summary = []

        for graph in self.original_summary:
            sorted_graph = {"graph_data": graph["graph_data"], "cell": []}
            
            for cell in graph["cell"]:
                sorted_cell = {"name_cell": cell["name_cell"], "exist": [], "none": []}
                
                for key, value in cell.items():
                    if key != "name_cell" and key != "measurement_condition":
                        if value is None:
                            sorted_cell["none"].append(key)
                        else:
                            sorted_cell["exist"].append(f"{key}: {value}")

                if "measurement_condition" in cell:
                    exist_cond = []
                    none_cond = []
                    for cond_key, cond_value in cell["measurement_condition"].items():
                        if cond_key == "C_rate":
                            if cond_value is None:
                                none_cond.append(cond_key)
                            else:
                                exist_cond.append(f"{cond_key}: {cond_value}")
                        else:
                            if 'value' not in cond_value:
                                cond_value = {'value': None, 'unit': None}
                            elif 'unit' not in cond_value:
                                cond_value['unit'] = None
                            if cond_value["value"] is None:
                                none_cond.append(cond_key)
                            else:
                                exist_cond.append(f"{cond_key}: {cond_value}")

                    if exist_cond:
                        sorted_cell["exist"].append(f"measurement_condition[{', '.join(exist_cond)}]")
                        
                    if none_cond:
                        sorted_cell["none"].append(f"measurement_condition[{', '.join(none_cond)}]")

                sorted_graph["cell"].append(sorted_cell)
            sorted_summary.append(sorted_graph)
        return sorted_summary

    def get_new_summary(self):        
        texts=[]
        revised_text=[]
        combined_indexs = list(dict(self.sub_).keys())
        combined_indexs.sort()
        for index in combined_indexs:
            texts.append(self.experimental_texts[index])
        combined_texts = ' '.join(texts)
        
        for revised_index in list(set(self.material + self.measurement)):
            revised_text.append(self.experimental_texts[revised_index])
        revised_combined_texts = ' '.join(revised_text)
        
        sorted_summary = self.preprocess_original_summary()        
        
        new_summary = []
        prompt = PromptTemplate.from_template(PROMPT_CELL)
        llm_cell = ChatOpenAI(temperature=0.0, model_name='gpt-4', openai_api_key=self.openai_api_key)
        for i in range(len(self.original_summary)):
            graph = copy.deepcopy(self.original_summary[i])
            figure_num = graph["graph_data"]["figure"]
            graph_label = graph["graph_data"]["graph_label"]
            new_graph = {}
            new_graph["graph_data"] = graph["graph_data"]
            num_of_cells = len(graph["cell"])
            cell_name_list = []
            exist_list = []
            none_list = []
            for j in range(num_of_cells):
                cell = graph["cell"][j]
                cell_name = cell["name_cell"]
                exist = sorted_summary[i]["cell"][j]["exist"]
                none = sorted_summary[i]["cell"][j]["none"]
                cell_name_list.append(cell_name)
                exist_list.append(', '.join(exist))
                none_list.append(', '.join(none))
            try:
                output = llm_cell.predict(prompt.format(num_of_cells=num_of_cells, figure_num=figure_num, graph_label=graph_label, 
                                                    cell_name=cell_name_list, exist=exist_list, none=none_list, 
                                                    paragraph=combined_texts))
            except:
                output = llm_cell.predict(prompt.format(num_of_cells=num_of_cells, figure_num=figure_num, graph_label=graph_label, 
                                                    cell_name=cell_name_list, exist=exist_list, none=none_list, 
                                                    paragraph=revised_combined_texts))
            new_graph["cell"] = json.loads(output)
            new_summary.append(new_graph)
        return new_summary
    
    def update_summary(self):
        new_summary = self.get_new_summary()
        updated_summary = copy.deepcopy(self.original_summary)
        for i in range(len(updated_summary)):
            original_graph = updated_summary[i]
            new_graph = new_summary[i]
            for original_cell in original_graph['cell']:
                new_cell = next((item for item in new_graph['cell'] if item['name_cell'] == original_cell['name_cell']), None)
                if new_cell:
                    for key, value in original_cell.items():
                        if value is None and key in new_cell:
                            original_cell[key] = new_cell[key]
                        elif key == "measurement_condition" and value is not None:
                            for cond_key, cond_value in value.items():
                                if cond_value is None or (isinstance(cond_value, dict) and cond_value.get("value") is None):
                                    if new_cell[key] and cond_key in new_cell[key]:
                                        original_cell[key][cond_key] = new_cell[key][cond_key]
        return updated_summary  
    
    def get_material_dictionary(self):
        material_dictionary = {"name_cell_list":set(), "name_cathode_list":set(), "name_electrolyte_list":set(), "name_anode_list":set(), "name_separator_list":set(), "name_current_collector_list":set(), "name_interlayer_list":set()}

        for graph in self.cell_summary:
            for cell in graph["cell"]:
                for material, name in cell.items():
                    if material == "measurement_condition":
                        continue
                    if name is None:
                        material_dictionary[f"{material}_list"].add(None)
                        continue
                    material_dictionary[f"{material}_list"].add(name)
                    
        for key, value in material_dictionary.items():
            if value == [None]:
                value = None
            if value is not None:
                material_dictionary[key] = list(value)
                if len(material_dictionary[key]) > 1:
                    if None in material_dictionary[key]:
                        material_dictionary[key].remove(None)
        return material_dictionary
    
    def get_summary_dict(self):
        summary_dict =  {"cathode":[], "electrolyte":[], "anode":[], "separator":[], "current_collector":[], "interlayer":[], "cycle_performance":[]}
        name_cell = self.material_dictionary["name_cell_list"]
        llm_extract = ChatOpenAI(temperature=0.0, model_name='gpt-4', openai_api_key=self.openai_api_key)
        for categories, text in self.sub_categories_dict.items():
            if not text:
                continue

            if categories ==  "cycle_performance":
                pass
            
            elif categories == "EIS":
                pass
            
            elif categories == "current_collector":
                loaded_prompt = get_prompt(categories)
                output = llm_extract.predict(loaded_prompt.format(paragraph=text, name_cell=name_cell))
                summary_dict[categories] = json.loads(output)    
                
            else:
                name_material_list = self.material_dictionary[f"name_{categories}_list"]
                if name_material_list == None or name_material_list == [None]:
                    
                    loaded_none_prompt = get_prompt(f"{categories}_not_mentioned")
                    output = llm_extract.predict(loaded_none_prompt.format(paragraph=text, name_cell=name_cell)) 
                    summary_dict[categories] = json.loads(output)        
                                
                else:
                    name_material = name_material_list
                    loaded_prompt = get_prompt(categories)
                    output = llm_extract.predict(loaded_prompt.format(paragraph=text, name_cell=name_cell, name_material=name_material))
                    summary_dict[categories] = json.loads(output)
        return summary_dict           
    
def get_prompt(property_str):
    prompt_module = importlib.import_module('libs.experimental.prompt') #prompt path
    prompt_var_name = f"PROMPT_{property_str.upper()}"
    return getattr(prompt_module, prompt_var_name, None)