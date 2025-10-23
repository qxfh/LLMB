from pathlib import Path
from bs4 import BeautifulSoup
import regex
import shutil


def has_XRD(caption):
    """return True if caption relate with XRD, else False"""    
    output = bool(regex.search(r"XRD|[xX].?ray.{0,3}diffraction", caption))
    
    return output


def has_subfigure(caption):
    re_analysis = regex.search(r"(SEM|TEM|XPS|[Rr]aman|[Cc]urrent[-/\s]voltage|AFM|isotherms|adsorption|desorption|ED|TGA|Tg|EDS|[Pp]ore size distribution|CV|[Mm]olecular structure)", caption)
    
    re_curve_spectrum = regex.search(r"(?<!(XRD|diffraction)\s?)(curve|spectr(um|a)|pattern)", caption)
    
    get_sub = regex.search(r"^\([Aa]", caption) or bool(regex.search(r"^[Aa](\-[b-zB-Z])?\)", caption))
    return bool(re_analysis or get_sub or re_curve_spectrum)
