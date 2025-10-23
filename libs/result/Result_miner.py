import json
import re
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from .prompt import PROMPT_RESULT, PROMPT_RESULT_REDUCE_TOKEN

class ResultMiner:
    def __init__(self, index, caption, texts, number_of_cells=None, openai_api_key=None):
        self.index = index
        self.caption = caption
        self.texts = texts
        self.number_of_cells = number_of_cells
        self.openai_api_key = openai_api_key
        self.graph_text_dict = self.get_graph_text_dict()
        self.graph_caption_dict = self.get_graph_caption_dict()
        self.caption_result_summary = self.get_caption_result_summary()
        
    def get_graph_text_dict(self):
        graph_text_dict = {} 
        index = self.index
        for figure_num, graph_label in index:
            graph_text_dict[figure_num] = find_graph_text(self.texts, figure_num)
        return graph_text_dict

    def get_graph_caption_dict(self):
        graph_caption_dict = {}
        index = self.index
        for figure_num, graph_label in index:
            graph_caption_dict[figure_num] = find_graph_caption(self.caption, figure_num)
        return graph_caption_dict
    
    def get_result_summary(self):
        result_summary = []
        prompt = PromptTemplate.from_template(PROMPT_RESULT)
        llm_result = ChatOpenAI(temperature=0.0, model_name='gpt-4', openai_api_key=self.openai_api_key)
        for figure_num, graph_label in self.index:
            output = llm_result.predict((prompt.format(figure_num = figure_num, graph_label = graph_label, paragraph = '\n'.join(self.graph_text_dict[figure_num]))))
            result_summary.append(json.loads(output))
        return result_summary

    def get_caption_result_summary(self):
        result_summary = []
        prompt = PromptTemplate.from_template(PROMPT_RESULT)
        llm_result = ChatOpenAI(temperature=0.0, model_name='gpt-4', openai_api_key=self.openai_api_key)
        for figure_num, graph_label in self.index:
            caption = ''.join(self.graph_caption_dict[figure_num])
            paragraph = '\n'.join(self.graph_text_dict[figure_num])
            try:
                output = llm_result.predict((prompt.format(figure_num = figure_num, graph_label = graph_label, caption = caption, paragraph = paragraph)))
            except:
                prompt = PromptTemplate.from_template(PROMPT_RESULT_REDUCE_TOKEN)
                output = llm_result.predict((prompt.format(figure_num = figure_num, graph_label = graph_label, caption = caption, paragraph = paragraph)))
            output = output.replace(u'\xa0', u' ')
            result_summary.append(json.loads(output))
        return result_summary

def generate_figure_patterns(num = None):
    if num: 
        return [
            rf'\bfig\.?\s*{num}[a-zA-Z]*\b', 
            rf'\bfigure\.?\s*{num}[a-zA-Z]*\b', 
            rf'\bFig\.?\s*{num}[a-zA-Z]*\b', 
            rf'\bFigure\.?\s*{num}[a-zA-Z]*\b',
        ]
    else:
        return [
            rf'\bfig\.?\s*\d+[a-zA-Z]*\b', 
            rf'\bfigure\.?\s*\d+[a-zA-Z]*\b', 
            rf'\bFig\.?\s*\d+[a-zA-Z]*\b', 
            rf'\bFigure\.?\s*\d+[a-zA-Z]*\b',
        ]

def find_graph_text(texts, figure_num): 
    figure_text = []
    patterns = generate_figure_patterns(figure_num)
    for text in texts:
        for figure_pattern in patterns:
            if re.search(figure_pattern, text):
                figure_text.append(text)
    return figure_text

def generate_caption_patterns(num = None):
    if num:
        return [
        rf'\{{{{fig\.\s*{num}\..*?}}}}',
        rf'\{{{{figure\.\s*{num}\..*?}}}}',
        rf'\{{{{Fig\.\s*{num}\..*?}}}}',
        rf'\{{{{figure\.\s*{num}\..*?}}}}',
    ]

def find_graph_caption(caption, figure_num):
    caption_texts = []
    patterns = generate_caption_patterns(figure_num)
    
    for figure_pattern in patterns:
        matches = re.findall(figure_pattern, caption, re.DOTALL)
        caption_texts.extend(matches)
    
    return caption_texts