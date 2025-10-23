import glob
import os
import random
import traceback
from libs.Preprocess import *
from libs.caption.Caption_miner import *
from libs.result.Result_miner import *
from libs.experimental.Experimental_miner import *
from libs.caption.prompt import *
from libs.result.prompt import *
from libs.experimental.prompt import *
from libs.merge.Cell_merge import *

random.seed(1557)

#example of config_num = "1"
#example of API_key_dict: {"1": API_key_1, "2": API_key_2}

class TextMining:
    def __init__(self, config_num, API_key_dict, first_index, last_index):
        self.config_num = config_num
        self.openai_api_key_dict = API_key_dict
        self.first_index, self.last_index = first_index, last_index
        self.paper_index_dict = {"1": [self.first_index, self.last_index]}
        xmls = glob.glob('elsevier_LMB_xml/*.xml')
        xmls.sort()
        self.Result, self.Error = self.text_mining(self.config_num)

    def text_mining(self):
        Result_dictionary = {}
        Error_dictionary = {}
        order = 0
        openai_api_key = self.openai_api_key_dict[self.config_num]
        index_list = self.paper_index_dict[self.config_num]
        
        for index in index_list:
            order += 1
            try:
                pp = Preprocessing(self.xmls[index])
            except Exception as P_E:
                err = traceback.format_exc()
                Error_dictionary[index] = {"Preprocessing_error": f"{str(P_E)}\n{err}"}
                
                continue
        
            file_path = pp.file_path
            path_check = file_path.replace('elsevier_LMB_xml/', 'elsevier_LMB_none_cycle_xml/')
            if os.path.exists(path_check):
                continue
                
            try:    # Review paper
                if len(glob.glob(f'{pp.get_image_path()}/*.png')) > 13:
                    Error_dictionary[index] = {"review_paper": file_path}
                    continue
            except:
                pass
            Result = {}
            Result["metadata"] = pp.metadata
            
            ## CaptionMiner
            try:
                cm = CaptionMiner(pp.caption, openai_api_key)
                if cm.cycle_figure_index == None:
                    continue
                else:
                    cm_index = cm.index
                    cm_cycle_figure_index = []
                    for figure_index, graph_label in cm_index:
                        cm_cycle_figure_index.append({'graph_data': {'figure': figure_index, 'graph_label': graph_label}})
            except:
                Error_dictionary[index] = {"CaptionMiner_error": file_path}
                continue
                
            if cm_cycle_figure_index == []:
                continue

            ## ResultMiner
            try:
                rm = ResultMiner(cm_index, pp.caption, pp.texts, openai_api_key=openai_api_key)
            except Exception as R_E:
                err = traceback.format_exc()
                Error_dictionary[index] = {"ResultMiner_error": f"{str(R_E)}\n{err}"}
                continue

            ## ExperimentalMine
            if pp.experimental_texts == None:
                Result["Existence_of_Experimental_paragraph"] = 0
                try:
                    Result["Result"] = rm.caption_result_summary
                    Result_dictionary[index] = Result
                    continue
                except Exception as R_E:
                    err = traceback.format_exc()
                    Error_dictionary[index] = {"Result_error with no experimental paragraph": f"{str(R_E)}\n{err}"}
                    continue
            else:
                try:
                    em = All_ExperimentalMiner(pp.experimental_texts, rm.caption_result_summary, openai_api_key=openai_api_key)
                    if not em.material and not em.measurement:
                        Result["Existence_of_Experimental_paragraph"] = 0
                        Result["Result"] = rm.caption_result_summary
                        Result_dictionary[index] = Result
                        continue
                    else:
                        Result["Existence_of_Experimental_paragraph"] = 1

                except Exception as E_E:
                    err = traceback.format_exc()
                    Error_dictionary[index] = {"ExperimentalMiner_error": f"{str(E_E)}\n{err}"}
                    continue
            
            ## Merging
            try:
                mg = Merge(em.cell_summary, em.summary_dict)
                Output = mg.merge_summary
                Result["Result"] = Output

            except Exception as M_E:
                err = traceback.format_exc()
                Error_dictionary[index] = {"Merging_error": f"{str(M_E)}\n{err}"}
                continue
                
            Result_dictionary[index] = Result
        return Result_dictionary, Error_dictionary