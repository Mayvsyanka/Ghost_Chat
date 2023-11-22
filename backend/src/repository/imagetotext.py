from pytesseract import image_to_string
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

async def convert(file_name, language):
    if language == 'english':
        lang = 'eng'
    elif language == 'ukrainian':
        lang = 'ukr'
    text = image_to_string(Image.open(file_name), lang=lang)
    return(text)
