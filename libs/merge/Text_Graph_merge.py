import json
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from .prompt import *

class MergeMiner_:
    def __init__(self, matching_dictionary, openai_api_key):
        self.matching_dictionary = matching_dictionary
        self.openai_api_key = openai_api_key
        self.preprocess_matching()
        self.matching_group1_ = self.get_matching_group1_()
        self.matching_group3_ = self.get_matching_group3_()
        self.matching_group4_ = self.get_matching_group4_()
    
    def preprocess_matching(self):
        self.group1 = preprocess_matching_dictionary(self.matching_dictionary["g>t"])
        self.group2 = preprocess_matching_dictionary(self.matching_dictionary["g==t==1"])
        self.group3 = preprocess_matching_dictionary(self.matching_dictionary["g<t"])
        self.group4 = preprocess_matching_dictionary(self.matching_dictionary["g==t!=1"])
        self.null_input = preprocess_matching_dictionary(self.matching_dictionary["null_input"])
        self.other = preprocess_matching_dictionary(self.matching_dictionary["other"])
    
    def get_matching_group1_(self):
        result = {}
        llm_figure = ChatOpenAI(temperature=0.0, model_name='gpt-4', openai_api_key=self.openai_api_key)
        prompt = PromptTemplate.from_template(PROMPT_MATCHING_GROUP1_)
        for index, value in self.group1.items():
            print("====",index,"====")
            graph_legend, cell_name = value
            output = llm_figure.predict((prompt.format(graph_legend=graph_legend, cell_name=cell_name)))
            output = output.replace("'", "\"")
            output_list = json.loads(output)
            result[index] = output_list
        return result

    def get_matching_group3_(self):
        result = {}
        llm_figure = ChatOpenAI(temperature=0.0, model_name='gpt-4', openai_api_key=self.openai_api_key)
        prompt = PromptTemplate.from_template(PROMPT_MATCHING_GROUP3_)
        for index, value in self.group3.items():
            print("====",index,"====")
            graph_legend, cell_name = value
            output = llm_figure.predict((prompt.format(graph_legend=graph_legend, cell_name=cell_name)))
            output = output.replace("'", "\"")
            output_list = json.loads(output)
            result[index] = output_list
        return result

    def get_matching_group4_(self):   
        result = {}
        llm_figure = ChatOpenAI(temperature=0.0, model_name='gpt-4', openai_api_key=self.openai_api_key)
        prompt = PromptTemplate.from_template(PROMPT_MATCHING_GROUP4_)
        for index, value in self.group4.items():
            print("====",index,"====")
            graph_legend, cell_name = value
            output = llm_figure.predict((prompt.format(graph_legend=graph_legend, cell_name=cell_name)))
            output = output.replace("'", "\"")
            output_list = json.loads(output)
            result[index] = output_list
        return result

def preprocess_matching_dictionary(matching_dictionary):
    merge_miner_input = {}
    if not matching_dictionary:
        return None
    for figure_file_path, value in matching_dictionary.items():
        index = figure_file_path
        g_t_input = [value["graph"],value["text"]]
        merge_miner_input[index] = g_t_input
    return merge_miner_input
