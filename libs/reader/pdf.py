from chemdataextractor import Document
from chemdataextractor.reader import PdfReader as CdeReader
from chemdataextractor.doc import Paragraph
from collections import defaultdict
import regex


from .reader_meta import Reader
from .error import ReaderError


class CDEPdfReader(Reader):
    suffix = '.pdf'
    
    @classmethod
    def parsing(cls, file):
        try:
            with open(file, 'rb') as f_cde:
                doc = Document.from_file(f_cde, readers=[CdeReader()])
            elements = [para for para in doc.elements if isinstance(para, Paragraph)]
        except Exception:
            raise ReaderError('ChemDataExtractor does not work. Please check your file.')

        if not elements:
            raise ReaderError('There are no paragraph in paper')
        return elements

    @classmethod
    def get_metadata(cls, file):
        metadata = defaultdict(type(None))
        elements = cls.parsing(file)
        
        for element in elements:
            text = element.text
            if regex.search(r"(?i)\bdoi\b", text):
                doi_search = regex.search(r"\b\d\d\.\d\d\d\d/\S+", text)
                if doi_search:
                    metadata['doi'] = doi_search.group()
                    return metadata

        return metadata
