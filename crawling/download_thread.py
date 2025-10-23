import os
from pathlib import Path
import urllib
import json
import requests
import regex
from threading import Thread
import time
import logging
import csv
import pandas as pd

from .elsevier_download import (
    elsevier_image_download, elsevier_text_download, get_figure_info
)


# api key
with open('api_key.txt') as f:
    api_key = f.read().strip()


def get_logger(filename, print_log=False):
    __logger = logging.getLogger(filename)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    
    # File handler : 파일 생성
    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(formatter)
    __logger.addHandler(file_handler)
    
    # Stream handler : Print와 같은 기능
    if print_log:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        __logger.addHandler(stream_handler)
    
    __logger.setLevel(logging.DEBUG)
    return __logger
    
    
def yield_url(doi_set, logger):
    for doi in doi_set:
        url = f'https://doi.org/{doi}'
        #logger.info(f'Start doi : {doi}')
        try:
            #response = opener.open(url)
            response = requests.get(url, timeout=60)
        except KeyboardInterrupt:
            logger.error('Keyboard Interrupt')
            return
        except Exception as e:
            logger.error(f'Error occured : ({type(e)}) {e}')
            data = ''
            journal = ''
        else:
            data = response.url
            regex_journal = regex.search(
                r'(acs|rsc|elsevier|sciencedirect|wiley|springer|nature)',
                data
            )
            if regex_journal:
                journal = regex_journal.group()
            else:
                journal = ''
        finally:  
            d = [doi, data, journal]
            yield d
        

class FindWorker(Thread):
    def __init__(self, doi_list, queue, journal_csv, log_file='find_doi.log', 
                 print_log=False, timestep=10):
        super().__init__()
        self.queue = queue
        self.elsevier_counter = 0
        self.csv = journal_csv
        self.doi_list = doi_list
        self.log_file = get_logger(log_file, print_log=print_log) 
        self.doi_set = self.get_doi_set(doi_list, journal_csv)
        self.timestep = timestep
        

    def write_row(self, data):
        with open(self.csv, 'a', newline='') as f:
            wr = csv.writer(f)
            wr.writerow(data)

    def get_doi_set(self, doi_list, journal_csv):
        if not os.path.exists(journal_csv):
            with open(journal_csv, 'w') as f:
                wr = csv.writer(f)
                wr.writerow(['doi', 'url', 'journal'])

        df = pd.read_csv(journal_csv)            
        
        # make doi_set
        doi_set = []
        with open(doi_list) as f:
            for line in f:
                line = line.strip()
                if line in doi_set:             # already exists
                    continue
                elif line in df['doi'].iloc():  # already find
                    self.log_file.info(f'{line} already find')
                    continue
                doi_set.append(line)

        # append elsevier-xml
        for doi in df['doi'][df['journal']=='elsevier']:
            self.queue.put(doi)

        return doi_set
        
    def run(self):
        self.log_file.info('Start : DOI Find worker')
        self.log_file.info(f'Number of set : {len(self.doi_set)}')
        
        # write first row
        
        data_iter = yield_url(self.doi_set, self.log_file)
        for i, data in enumerate(data_iter):
            doi, url, journal = data

            if i % self.timestep == 0:
                self.log_file.info(f'Search-doi : {i} | Elsevier-doi : {self.elsevier_counter}')
            
            # write_row
            if url:
                self.write_row(data)

            # find elseiver-journal
            if journal == 'elsevier':
                self.elsevier_counter += 1
                self.queue.put(doi)
                self.log_file.info(f'{doi} : Queued to download xml')
                
        self.queue.put('Done')
        self.log_file.info('Finished to search doi') 
        

class DownloadWorker(Thread):
    def __init__(self, queue, output_queue, sleep_time=20, outdir='./output_xml',
                 log_file='download_xml.log', print_log=False):
        super().__init__()
        self.queue = queue
        self.sleep_time = sleep_time
        self.output_queue = output_queue
        self.outdir = Path(outdir)
        self.log_file = get_logger(log_file, print_log=print_log)

    def get_name(self, doi):
        doi_name = doi.replace("/", "_")
        output_name = self.outdir/f'{doi_name}.xml'
        return output_name
        
    def func(self, doi):
        self.log_file.info(f'Download XML : {doi} start')

        # get name
        output_name = self.get_name(doi)

        # already downloaded
        if output_name.exists():
            self.log_file.info(f"Download XML : {doi} already existed")
            return doi
        
        # download text
        try:
            elsevier_text_download(api_key, doi, output_name)
            self.log_file.info(f'Download XML : {doi} dowload succeed')
            time.sleep(self.sleep_time)
            self.log_file.info("XML : finish sleep")
            return doi

        except KeyboardInterrupt:
            return None

        except Exception as e:
            self.log_file.info(f"Download XML : {doi} download failed ({type(e)} | {e})")
        
    def run(self):
        self.log_file.info('Start : XML Download worker')
        
        # run roop for queued XML 
        while True:
            doi = self.queue.get()
            if doi == 'Done':
                self.output_queue.put('Done')
                self.log_file.info('Finished : XML Download worker')
                return
            
            output = self.func(doi)
            if output:
                self.output_queue.put(output)
                
                
class ImageDownloadWorker(Thread):
    def __init__(self, queue, sleep_time=20, indir='./output_xml', 
                 outdir='./output_image', log_file='download_image.log',
                 print_log=False, func_caption_filter=None):
        super().__init__()
        self.queue = queue
        self.indir = Path(indir)
        self.outdir = Path(outdir)
        self.sleep_time = sleep_time
        self.log_file = get_logger(log_file, print_log=print_log)

        if func_caption_filter is None:
            self.func_caption_filter = (lambda t: True)
        else:
            self.func_caption_filter = func_caption_filter 

    def func(self, doi):
        self.log_file.info(f'Image : Download_queue : {doi}')
        
        doi_name = doi.replace("/", "_")
        input_name = self.indir/f'{doi_name}.xml'

        figures = get_figure_info(input_name)

        img_folder = self.outdir/doi_name
        img_folder.mkdir(exist_ok=True, parents=True)

        with open(img_folder/'metadata.json', 'w') as f:
            json.dump(figures, f)

        for figure in figures:
            caption = figure['caption']
            ref = figure['locator']
            mimetype = figure['mimetype'][0].split("/")[1]
            
            if not self.func_caption_filter(caption):
                continue

            file_name = img_folder/f'{ref}.{mimetype}'

            # already exists
            if file_name.exists():
                self.log_file.info(f"Image : {doi}-{ref} already exists")
                continue

            # download image
            try:
                elsevier_image_download(api_key, doi, ref, file_name, file_format=mimetype, quality='standard')
                self.log_file.info(f"Image : {doi} download succeed")
                time.sleep(self.sleep_time)
                self.log_file.info(f'Image : finish sleep')
            except KeyboardInterrupt:
                return
            except Exception:
                self.log_file.info(f"Image : {doi} download failed")
        
    def run(self):
        self.log_file.info('Start : Image Download worker')

        # run roop
        while True:
            doi = self.queue.get()
            if doi == 'Done':
                self.log_file.info('Finish : XML Download worker')
                return
            output = self.func(doi)
            
