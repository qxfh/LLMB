import os
from pathlib import Path
from queue import Queue
import time
import pandas as pd

from .download_thread import ImageDownloadWorker, FindWorker, DownloadWorker
from .get_xrd_paper import has_subfigure, has_XRD



def download_image_from_xml(xml_folder='./output_xml', 
                            image_folder='./output_image',
                            image_logfile='download_image.log', 
                            func_caption_filter=None, 
                            sleep_time=20,
                            print_log=False):

    """Download elsevier image from downloaded xml file
    :param input_folder : (str, or Path) a directory path that has xml files
    :param output_folder : (str, or Path) a directory path where the output file will be stored.
    :param logfile : (str, or Path) file name to record progress (ex: log.txt)
    :param sleep_time : (int) The interval time (second) between downloads. default is 20
    :param func_caption_filter : (func) Image filter function with caption as input and bool as output. default is None. If None, download all images.
    """
    
    Path(image_folder).mkdir(exist_ok=True, parents=True)
    files = Path(xml_folder).glob('*.xml')
    img_queue = Queue()
    for file in files:
        img_queue.put(file.stem)
    img_queue.put('Done')

    thread3 = ImageDownloadWorker(queue=img_queue, sleep_time=sleep_time, 
                                 indir=xml_folder, outdir=image_folder,
                                 log_file=image_logfile, print_log=print_log,
                                 func_caption_filter=func_caption_filter)      
    
    thread3.start()
    thread3.join()
   

def download_xml_from_doi(doi_list, 
                          xml_folder='./output_xml', 
                          find_logfile='find_doi.log',
                          xml_logfile='download_xml.log', 
                          journal_csv='journal.csv',  
                          sleep_time=20,
                          timestep=10,
                          print_log=False):

    """Download elsevier image from downloaded xml file
    :param doi_list : (str, or Path) file name that have doi list
    :param xml_folder : (str, or Path) a directory path that has xml files
    :param logfile : (str, or Path) file name to record progress (ex: log.txt)
    :param sleep_time : (int) The interval time (second) between downloads. default is 20
    """
    
    if not os.path.exists(doi_list):
        raise ValueError(f'{doi_list} does not exists')

    Path(xml_folder).mkdir(exist_ok=True, parents=True)

    doi_queue = Queue()
    out_queue = Queue()
    
    thread1 = FindWorker(doi_list=doi_list, queue=doi_queue, 
                         journal_csv=journal_csv, log_file=find_logfile, 
                         timestep=timestep, print_log=print_log)
    thread2 = DownloadWorker(queue=doi_queue, output_queue=out_queue,
                            outdir=xml_folder, sleep_time=sleep_time,
                            log_file=xml_logfile, print_log=print_log)
    
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
    
    
def download_xml_and_images_from_doi(doi_list, 
                                     xml_folder='./output_xml', 
                                     image_folder='./output_image', 
                                     find_logfile='find_doi.log',
                                     xml_logfile='download_xml.log',
                                     image_logfile='download_image.log',
                                     journal_csv='journal.csv', 
                                     func_caption_filter=None, 
                                     sleep_time=20,
                                     timestep=10,
                                     print_log=False,
                                     ):

    """Download elsevier image from downloaded xml file
    :param doi_list : (str, or Path) file name that have doi list
    :param xml_folder : (str, or Path) a directory path that has xml files
    :param image_folder : (str, or Path) a directory path where the output file will be stored.
    :param logfile : (str, or Path) file name to record progress (ex: log.txt)
    :param journal_csv : (str, or Path) csv file for saving journal of doi
    :param func_caption_filter : (func) Image filter function with caption as input and bool as output. default is None. If None, download all images.
    :param sleep_time : (int) The interval time (second) between downloads. default is 20
    """
   
    if not os.path.exists(doi_list):
        raise ValueError(f'{doi_list} does not exists')

    Path(xml_folder).mkdir(exist_ok=True, parents=True)
    Path(image_folder).mkdir(exist_ok=True, parents=True)
    
    doi_queue = Queue()
    img_queue = Queue()
    
    thread1 = FindWorker(doi_list=doi_list, queue=doi_queue, 
                         journal_csv=journal_csv, log_file=find_logfile, 
                         timestep=timestep, print_log=print_log)
    thread2 = DownloadWorker(queue=doi_queue, output_queue=img_queue,
                            outdir=xml_folder, sleep_time=sleep_time, 
                            log_file=xml_logfile, print_log=print_log)
    thread3 = ImageDownloadWorker(queue=img_queue, sleep_time=sleep_time, 
                                 indir=xml_folder, outdir=image_folder,
                                 log_file=image_logfile, print_log=print_log,
                                 func_caption_filter=func_caption_filter)
    
    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()
