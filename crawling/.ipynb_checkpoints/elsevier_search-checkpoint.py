import requests
import json
from crawling.elsevier_download import DownloadError

with open('api_key.txt') as f:
    api_key = f.read()

def elsevier_search(api_key, query, **kwargs):
    """Search image for elsevier journal
    
    Attributes:
        DOI : (str) doi of paper
        ref : (str) Reference of image in XML file. ex) gr1, gr2
        output : (str) output filename. ex) test.xml
        api_key : (str) api key for Elsevier Devloper Potal. (https://dev.elsevier.com/)
    
    Return:
        (str) xml file of paper
    """
    
    URL = 'https://api.elsevier.com/content/search/scopus'
    
    headers = {"X-ELS-APIKey"  : api_key,
              "Accept"          : f'application/json'}
    
    query = { 'query'           : query,
             'count'          : kwargs.get('count', 200),
             **kwargs}
    
    r = requests.get(URL,headers = headers, params=query)
    
    status = r.status_code
    
    if not status == 200:
        raise DownloadError(r.status_code)
    
    return json.loads(r.text)


def get_doi_from_elsevier_search(api_key, query, **kwargs):
    doi_list = []
    for year in range(2003, 2022):
        start_num=0
        
        while True:
            try:
                search_result = elsevier_search(api_key, date=str(year), query=query, field='doi', start=start_num)
            except DownloadError as e:
                print (year, start_num, e)
                break
            else:
                entry = search_result['search-results']['entry']
                doi_list += [dev['prism:doi'] for dev in entry if 'prism:doi' in dev]

                if len(entry) < 200:
                    break
            finally:
                    start_num += 200
        
    return doi_list
    
    
if __name__ == '__main__':
    doi_list = get_doi_from_elsevier_search(api_key, query='KEY(metal organic framework)')