# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

def str_transliterate(s):
    s = re.sub("[á|à|â|ä|å]", "a", s)
    s = re.sub("[Á|À|Â|Ã|Ä|Å]", "A", s)
    s = re.sub("[é|è|ê|ë|Ø]", "e", s)
    s = re.sub("[É|È|Ë|Ê]", "E", s)
    s = re.sub("[ó|ò|ö|ô]", "o", s)
    s = re.sub("[Ò|Ó|Ô|Õ|Ö]", "O", s)
    s = re.sub("[ù|ú|ü|û|ß]", "u", s)
    s = re.sub("[Ù|Ú|Û|Ü]", "U", s)
    s = re.sub("[º||©|'|’|®]", " ", s)
    return s
    
def mm_to_mmm(mm):
    """Convert month in numbre to letter
    >>> mm_to_mmm("10")
    'Octobre'
    """
    liste_mois =  {"01": "Janvier", "02": "Fevrier", "03": "Mars", "04": "Avril", "05": "Mai", "06": "Juin", "07": "Juillet", "08": "Aout", "09": "Septembre", "10": "Octobre", "11": "Novembre", "12": "Decembre"}
    return liste_mois.get(mm, None)
    
def mmm_to_mm(mmm):
    """Convert month in letter to number
    >>> mmm_to_mm("Octobre")
    '10'
    >>> mmm_to_mm("Février")
    '02'
    """
    mmm = str_transliterate(mmm.lower())
    liste_mois =  {"janvier": "01", "fevrier": "02", "fevr": "02", "mars": "03", "avril": "04", "mai": "05", "juin": "06", "juillet": "07", "aout": "08", "septembre": "09", "octobre": "10", "novembre": "11", "decembre": "12"}
    return liste_mois.get(mmm, None)
    
def jjj_to_jj(jjj):
    """Convert day in letter to number
    >>> jjj_to_jj("Mardi")
    '02'
    """
    jjj = str_transliterate(jjj.lower())
    ls_jour = {"lundi": "01", "mardi": "02", "mercredi": "03", "jeudi": "04", "vendredi": "05", "samedi": "06", "dimanche": "07"}
    return ls_jour.get(jjj, None)

def pdf_to_txt(path):
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfpage import PDFPage
    from io import StringIO
    
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=laparams)
    with open(path, 'rb') as fp:
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()
    
        try:
            for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
                interpreter.process_page(page)
        except:
            return ''
    
        text = retstr.getvalue()
    device.close()
    retstr.close()
    return text

def image_to_txt(pdf_path):
    import pdf2image
    from PIL import Image
    import pytesseract
    
    #DECLARE CONSTANTS
    DPI = 200
    OUTPUT_FOLDER = None

    pil_images = pdf2image.convert_from_path(pdf_path, dpi=DPI, output_folder=OUTPUT_FOLDER, fmt='jpg', thread_count=1, strict=False)
    res = []
    for image in pil_images:
        # image.save("/sharedfolders/nas/page_" + str(index) + ".jpg")
        # tmp_img = Image.open("/sharedfolders/nas/page_" + str(index) + ".jpg")
        res.append(pytesseract.image_to_string(image))
    return " ".join(res)