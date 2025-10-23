from bs4 import BeautifulSoup
from chemdataextractor import Document
from chemdataextractor.doc import Paragraph, Heading
from collections import defaultdict
import regex

from .reader_meta import Reader
from .error import ReaderError


class ElsevierXmlReader(Reader):
    """Target Journal : Elsevier"""
    suffix = '.xml'
    
    @classmethod
    def parsing(cls, file):
        elements = []
        text_list = []
        with open(file, 'r', encoding='UTF8') as f:
            soup = BeautifulSoup(f, 'lxml')
        for element in soup.find_all(["ce:abstract-sec", "ce:para", 'ce:section-title']):
            
            # Replace the <ce:cross-ref> tags with their text content
            for cross_ref in element.find_all("ce:cross-ref"):
                cross_ref.replace_with(cross_ref.text)
            
            # Remove the other tags you've mentioned
            for hyperlink in element.find_all(["ce:cross-refs", "ce:footnote", "ce:footnotes"]):
                hyperlink.extract()
                
            text = _cleanup_tag(element)

            if not text or text in text_list:
                continue
            elif element.name in ["ce:abstract-sec", "ce:para"]:
                element = Paragraph(text)
            elif element.name in ['ce:section-title']:
                element = Heading(text)
            else:
                raise ReaderError('Can not parse these paper')

            elements.append(element)
            text_list.append(text)
            
        if not elements:
            raise ReaderError('There are no paragraph in paper')

        return elements

    
    @classmethod
    def get_metadata(cls, file):
        with open(file, 'r',encoding='UTF8') as f:
            soup = BeautifulSoup(f.read(), "lxml")

        metadata = defaultdict(type(None))

        try:
            metadata['doi'] = soup.find("dc:identifier").text.replace("doi:", "")
        except AttributeError:
            pass
        try:
            metadata['title'] = soup.find("dc:title").text.strip()
        except AttributeError:
            pass
        try:
            metadata['journal'] = soup.find('prism:publisher').text
        except AttributeError:
            pass
        try:
            metadata['date'] = soup.find("prism:coverdate").text
        except AttributeError:
            pass
        try:
            metadata['author_list'] = [creator.text for creator in soup.find_all("dc:creator")]
        except AttributeError:
            pass
            
        return metadata


class GeneralXmlReader(Reader):
    """Target Journal : ACS, Springer, Nature"""
    suffix = '.xml'

    @classmethod
    def parsing(cls, file):
        elements = []
        text_list = []
        with open(file, 'r',encoding='UTF8') as f:
            soup = BeautifulSoup(f, 'lxml')

        if soup.find('sec'):
            for tags in soup.find_all(['abstract', "sec", "note"]):
                for element in tags.find_all(['caption', 'table-wrap-foot', 'table', 'fig', 'alternatives', 'alternative',
                                              'footnote']):
                    element.extract()

                for element in tags.find_all(['p', 'title']):
                    for hyperlink in element.find_all(["named-content", "xref"]):
                        hyperlink.extract()

                    text = _cleanup_tag(element)
                    if not text or text in text_list:
                        continue
                    elif element.name == 'p':
                        element = Paragraph(text)
                    elif element.name == 'title':
                        element = Heading(text)
                    else:
                        raise ReaderError('Can not parse these paper')
                    elements.append(element)
                    text_list.append(text)
        else:
            for element in soup.find_all(['caption', 'table-wrap-foot', 'table', 'fig', 'alternatives', 'alternative',
                                          'footnote', 'api-response']):
                element.extract()

            for element in soup.find_all(['p', 'title']):
                for hyperlink in element.find_all(["named-content", "xref"]):
                    hyperlink.extract()

                if element.find('response'):
                    continue

                text = _cleanup_tag(element)
                if not text or text in text_list:
                    continue
                elif element.name == 'p':
                    element = Paragraph(text)
                elif element.name == 'title':
                    element = Heading(text)
                else:
                    raise ReaderError('Can not parse these paper')
                elements.append(element)
                text_list.append(text)
                
        for ref in soup.find_all('ref'):
            notes = ref.find_all(['note', 'p', 'comment', 'mixed-citation'])
            for note in notes:
                num_note = [p_ for p_ in note.parent.children if p_ != '\n']
                if len(num_note) <= 2:
                    text = _cleanup_tag(note)
                    if not text or text in text_list:
                        continue
                    else:
                        element = Paragraph(text)
                        elements.append(element)
                        text_list.append(text)

        return elements
    
    @classmethod
    def get_metadata(cls, file):
        with open(file, 'r',encoding='UTF8') as f:
            soup = BeautifulSoup(f.read(), "lxml")

        metadata = defaultdict(type(None))
        try:
            metadata['doi'] = soup.find('article-id', attrs={'pub-id-type': 'doi'}).text
        except AttributeError:
            pass
        try:
            metadata['title'] = soup.find('title-group').text
        except AttributeError:
            pass
        try:
            date_tag = soup.find('pub-date', attrs={'publication-format': 'electronic'})
            year = date_tag.find('year').text
            month = date_tag.find('month').text.zfill(2)
            day = date_tag.find('day').text.zfill(2)
            metadata['date'] = f"{year}.{month}.{day}"
        except AttributeError:
            pass
        try:
            metadata['journal'] = soup.find('publisher-name').text
        except AttributeError:
            pass
        try:
            metadata['author_list'] = [creator.find('name').text.strip() for creator in soup.find_all("contrib")]
        except AttributeError:
            pass

        return metadata
    
    
class CDEXmlReader(Reader):
    suffix = '.xml'

    @classmethod
    def parsing(cls, file):
        try:
            with open(file, 'rb') as f_cde:
                doc = Document.from_file(f_cde)
            elements = [para for para in doc.elements if isinstance(para, Paragraph)]
        except Exception:
            raise ReaderError('ChemDataExtractor does not work. Please check your file.')

        if not elements:
            raise ReaderError('There are no paragraph in paper')
        return elements
    
    @classmethod
    def get_metadata(cls, file):
        with open(file, 'r') as f:
            soup = BeautifulSoup(f.read(), "lxml")

        metadata = defaultdict(type(None))
        try:
            metadata['doi'] = soup.find('article-id', attrs={'pub-id-type': 'doi'}).text
        except AttributeError:
            pass
        try:
            metadata['title'] = soup.find('title-group').text
        except AttributeError:
            pass
        try:
            date_tag = soup.find('pub-date', attrs={'publication-format': 'electronic'})
            year = date_tag.find('year').text
            month = date_tag.find('month').text.zfill(2)
            day = date_tag.find('day').text.zfill(2)
            metadata['date'] = f"{year}.{month}.{day}"
        except AttributeError:
            pass
        try:
            metadata['journal'] = soup.find('publisher-name').text
        except AttributeError:
            pass
        try:
            metadata['author_list'] = [creator.find('name').text.strip() for creator in soup.find_all("contrib")]
        except AttributeError:
            pass
            
        return metadata

    
def _cleanup_tag(element):
    remove_space = regex.sub(r"(?<=<.+?>)\n(?=<.+?>)", "", str(element))
    #print(remove_space)
    text = BeautifulSoup(remove_space, 'lxml').get_text()
    return text.replace("\n", " ")


#원본 parsing 함수 
''' 
    @classmethod
    def parsing(cls, file):
        elements = []
        text_list = []
        with open(file, 'r', encoding='UTF8') as f:
            soup = BeautifulSoup(f, 'lxml')
        print(soup)
        for element in soup.find_all(["ce:abstract-sec", "ce:para", 'ce:section-title']):
            for hyperlink in element.find_all(["ce:cross-refs", "ce:cross-ref", "ce:footnote", "ce:footnotes"]):
                hyperlink.extract()
                
            text = _cleanup_tag(element)

            if not text or text in text_list:
                continue
            elif element.name in ["ce:abstract-sec", "ce:para"]:
                element = Paragraph(text)
            elif element.name in ['ce:section-title']:
                element = Heading(text)
            else:
                raise ReaderError('Can not parse these paper')

            elements.append(element)
            text_list.append(text)
            
        if not elements:
            raise ReaderError('There are no paragraph in paper')

        return elements

'''