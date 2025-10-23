import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image


class DownloadError(Exception):
    """Download Error"""
    def __init__(self, error_code : int):
        """Attributes:
        error_code : status code of requests from url
        """
        
        error_text = {
            400:'Invalid Request: This is an error that occurs when invalid information is submitted.',
            401:'Authentication Error: This is an error that occurs when a user cannot be authenticated due to missing/invalid credentials (authtoken or APIKey).',
            403:'Authorization/Entitlements Error: This is an error that occurs when a user cannot be authenticated or entitlements cannot be validated.',
            404:'Resource Not Found Error: This is an error that occurs when the requested resource cannot be found.',
            405:'Invalid HTTP Method: This is an error that occurs when the requested HTTP Method is invalid.',
            406:'Invalid Mime Type: This is an error that occurs when the requested mime type is invalid.',
            429:'Quota Exceeded: This is an error that occurs when a requester has exceeded the quota limits associated with their API Key.',
            500:'Generic Error: This is a general purpose error condition, typically due to back-end processing errors.'
        }
        
        super().__init__(error_text[error_code])
     
    
def elsevier_text_download(api_key, doi, output='test.xml'):
    """Download text for elsevier journal
    
    Attributes:
        doi : (str) doi of paper
        output : (str) output filename. ex) test.xml
        api_key : (str) api key for Elsevier Devloper Potal. (https://dev.elsevier.com/)
        
    Return:
        (str) xml file of paper
    """
    
    url = f'https://api.elsevier.com/content/article/doi/{doi}'
    
    headers = {"X-ELS-APIKey"  : api_key,
            "Accept"        : 'text/xml'}
    
    r = requests.get(url, headers = headers)
    
    if r.status_code != 200:
        raise DownloadError(r.status_code)
    
    with open(output, 'w') as f:
        f.write(r.text)
    
    return r.text


def elsevier_image_download(api_key, DOI, ref, output='test.gif', file_format='gif', quality='standard'):
    """Download image for elsevier journal
    
    Attributes:
        DOI : (str) doi of paper
        ref : (str) Reference of image in XML file. ex) gr1, gr2
        output : (str) output filename. ex) test.xml
        api_key : (str) api key for Elsevier Devloper Potal. (https://dev.elsevier.com/)
    
    Return:
        (str) xml file of paper
    """
    
    URL = f'https://api.elsevier.com/content/object/doi/{DOI}/ref/{ref}/{quality}'
    
    if 'image/' not in file_format:
        file_format = f'image/{file_format}'
    
    headers = {"X-ELS-APIKey"  : api_key,
              "Accept"          : file_format}
    
    r = requests.get(URL,headers = headers)
    
    status = r.status_code
    
    if not status == 200:
        raise DownloadError(r.status_code)
    
    img = Image.open(BytesIO(r.content))
    img.save(output)
    
    return img


def get_figure_info(file):
    captions = []
    with open(file, 'r') as f:
        soup = BeautifulSoup(f, 'lxml')
    
    for element in soup.find_all('ce:figure'):
        try:
            label = element.find('ce:label', recursive=False).text.strip().replace("\n","")
            locator = element.find('ce:link', recursive=False)['locator']    
            caption = element.find('ce:caption', recursive=False).text.strip().replace("\n","")

            
            mimetypes = [mime['mimetype'] for mime in soup.find_all('object', ref=locator, category="high")]    
            quality = 'high'
            if not mimetypes:
                mimetypes = [mime['mimetype'] for mime in soup.find_all('object', ref=locator, category="standard")]    
                quality = 'standard'
            #mimetypes = [mime['mimetype'] for mime in soup.find_all('object', ref=locator, category="standard")]
            captions.append({'label':label, 'locator':locator, 'caption':caption, 'mimetype':mimetypes, 'quality':quality})
        except KeyboardInterrupt:
            break
        except Exception:
            continue
        
    return captions


if __name__ == '__main__':
    #DOI = '10.1016/j.egyr.2023.01.121'
    #with open('../api_key.txt') as f:
    #    api_key = f.read().strip()
    #elsevier_text_download(api_key, DOI, 'test.xml')

    file = '/usr/storage/dudgns1675/data/mofpapers/synthesis/Elsevier_XML/10.1016_j.ultsonch.2018.02.048.xml'
    caption = get_figure_info(file)

    print (caption)

