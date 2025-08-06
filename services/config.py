"""
    Arquivo responsável por configurar o PATH do Tesseract OCR
"""

import pytesseract
import platform

def configure_tesseract():

    """
        Configura o caminho do executável do Tesseract OCR de acordo com o local de execução.

        Isso é necessário para que o pytesseract consiga invocar
        corretamente o OCR nativo instalado no sistema.
        
    """

    if platform.system() == "Windows":
        pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
    else:
        pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"