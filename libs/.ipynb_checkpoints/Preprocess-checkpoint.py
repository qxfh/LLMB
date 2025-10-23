import json
from pathlib import Path
from libs.reader import CDEPdfReader, ElsevierXmlReader
from chemdataextractor.doc import Paragraph, Heading, Title

class Preprocessing:
    def __init__(self, file_path):
        self.file_path = file_path
        self.reader = self.load_reader()
        self.caption = self.get_caption()
        self.paras = self.parsing()
        self.texts = self.get_texts()
        self.metadata = self.get_metadata()
        self.experimental_texts = self.get_experimental_texts()

    def get_image_path(self):
        image_folder = Path('./elsevier_LMB_image')
        image_path = image_folder / Path(self.file_path).stem
        if not image_path.exists(): 
            raise FileNotFoundError(f"No such file or directory: '{image_path}'")
        return image_path
    
    def check_file_type(self): #pdf or xml
        if self.file_path.endswith('.pdf'):
            return 'pdf'
        elif self.file_path.endswith('.xml'):
            return 'xml'
        else:
            raise ValueError('File type not supported.')
        
    def load_reader(self):
        file_type = self.check_file_type()
        if file_type == 'pdf':
            return CDEPdfReader()
        elif file_type == 'xml':
            return ElsevierXmlReader()
        
    def get_caption(self):
        image_path = self.get_image_path()
        caption_json_dir = image_path / Path('captions.json')
        with open(caption_json_dir, 'r') as f:
            caption_json = json.load(f)
        captions = ''
        for caption_dict in caption_json:
            captions += '{{' + caption_dict['label'] + '. ' + caption_dict['caption'] + '}} ' + '\n '
        return captions           

    def parsing(self):
        return self.reader.parsing(self.file_path)
        
    def get_metadata(self):
        return self.reader.get_metadata(self.file_path)
    
    def get_title(self):
        return self.metadata['title']
        
    def get_texts(self):
        return [paragraph.text for paragraph in self.paras]
    
    def get_headings(self):
        return [element.text for element in self.paras if isinstance(element, Heading)]

    def extract_headings(self):
        headings = self.get_headings()
    
        start_keywords = ["exp", "method", "material"]
        end1_keywords = ["result", "acknowledge", "conclus", "supplement", "credit", "discussion"]
        end2_keywords = ["references", "reference"]

        start_heading = next((h for h in headings if any(kw in h.lower() for kw in start_keywords) and len(h) <= 35), None)
        if start_heading != None:
            if "supple" in start_heading.lower():
                start_heading = None                

        if start_heading:
            start_index = headings.index(start_heading)
            end1_heading = next((h for h in headings[start_index+1:]
                                if h.lower() in end2_keywords or any(kw in h.lower() for kw in end1_keywords)), None)
        
        else:
            end1_heading = None
        return start_heading, end1_heading

    def get_experimental_texts(self):
        start_heading, end_heading = self.extract_headings()
        experimental_texts = []
        capture_text = False
        current_text = ""
    
        for element in self.paras:
            if isinstance(element, Heading):
                if element.text == start_heading:
                    capture_text = True
                    continue
                elif element.text == end_heading:
                    if current_text:
                        experimental_texts.append(current_text)
                    break
                elif capture_text:
                    if capture_text != "":
                        experimental_texts.append(current_text)
                    else:
                        pass
                    current_text = element.text + '.'
    
            elif capture_text and isinstance(element, Paragraph):
                current_text += " " + element.text       

        if not experimental_texts:
            print("Check start and end heading")
            return
        return experimental_texts