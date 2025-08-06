"""
    Módulo responsável por processar as imagens recebidas, e retornar o texto extraído e corrigido.
    Utiliza as bibliotecas Pillow e PIL para manipulação de imagens e pytesseract para OCR.
"""

# importações de bibliotecas necessárias nos tratamentos
from PIL import Image as PilImage, ExifTags, ImageFilter, ImageOps
import pytesseract
from io import BytesIO
from spellchecker import SpellChecker

# importando a biblioteca pillow_heif para suportar imagens HEIC
import pillow_heif
pillow_heif.register_heif_opener()

# importando o config.py para configurar o pytesseract
from services.config import configure_tesseract 
configure_tesseract()

class ImageProcessor:
    def __init__(self, image_file):
        """
            Inicializa o objeto ImageProcessor com um arquivo de imagem.

            Args:
                image_file (FileStorage): Imagem recebida via upload.
        """
        self.image_file = image_file
    
    def process_image(self):
        """
            Executa o pipeline de processamento da imagem:

            - Corrige orientação com base nos metadados EXIF
            - Converte para escala de cinza, redimensiona e binariza
            - Realça o contraste e aplica nitidez
            - Executa OCR com pytesseract
            - Corrige ortografia do texto extraído

            Returns:
                str: Texto corrigido extraído da imagem, ou mensagem de erro.
        """
        try:
            self.image_file.seek(0) # Reseta o ponteiro do arquivo para o início
            image = PilImage.open(BytesIO(self.image_file.read())) # Lê a imagem do arquivo

            image = self._correct_orientation(image) # Corrige a orientação da imagem
            image = image.convert('L') # Converte a imagem para escala de cinza
            image.thumbnail((800, 800)) # Redimensiona a imagem para um tamanho máximo de 800x800 pixels
            image = ImageOps.autocontrast(image) # Aplica contraste automático para melhorar a legibilidade

            threshold = 160 # Define um limiar para binarização
            image = image.point(lambda p: 255 if p > threshold else 0) # Binariza a imagem
            image = image.filter(ImageFilter.SHARPEN) # Aplica um filtro de nitidez para melhorar a qualidade da imagem

            # Extrai texto com pytesseract
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(image, lang='por', config=custom_config)

            # Corrige texto extraído
            corrected_text = self._correct_text(text)

            return corrected_text

        except Exception as e:
            return f"[ERRO] Não foi possível processar a imagem: {str(e)}"

    def _correct_orientation(self, image):
        """
            Corrige a orientação da imagem com base nas informações EXIF,
            ajustando rotações comuns de imagens tiradas por celulares.

            Args:
                image (PIL.Image): Imagem original.

            Returns:
                PIL.Image: Imagem com orientação corrigida.
        """
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break

            exif = image._getexif()
            if exif is not None:
                orientation_value = exif.get(orientation, None)

                if orientation_value == 3:
                    image = image.rotate(180, expand=True)
                elif orientation_value == 6:
                    image = image.rotate(270, expand=True)
                elif orientation_value == 8:
                    image = image.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            pass
        return image

    def _correct_text(self, text):

        """
            Corrige o texto extraído da imagem utilizando a biblioteca SpellChecker.

            Adiciona palavras personalizadas ao dicionário (nomes químicos e ingredientes)
            para evitar correções indevidas.

            Args:
                text (str): Texto cru extraído do OCR.

            Returns:
                str: Texto corrigido.
        """
        spell = SpellChecker(language='pt')

        custom_words = [
            "aqua",
            "water",
            "glycerin",
            "cetyl alcohol",
            "parfum",
            "fragrance",
            "glyceryl stearate",
            "ingredientes",
            "Cloreto de cobalto",
            "Azul cobalto",
            "Cloreto de cobalto (II) hexahidratado",
            "Cloreto de cobalto hexaidratado",
            "Cobalt dichloride",
            "Cobalt muriate",
            "Cobaltous chloride",
            "Dichlorocobalt",
            "Dicloreto de cobalto hexahidratado",
            "Sulfato de níquel",
            "Nickel(II) sulfate",
            "Nickel sulfate",
            "NiSO₄",
            "Sulfato de níquel(II)",
            "Sulfato de níquel heptaidratado",
            "Sulfato de níquel hexahidratado",
            "Sulfato níqueloso",
            "Tetracloropaladato de sódio",
            "Cloridrato de sódio de paládio",
            "Disodium tetrachloropalladate",
            "Palladium sodium chloridetrihydrate",
            "Sodium tetrachloropalladate",
            "Sodium tetrachloropalladate (II)",
            "Tetracloropaladato dissódico",
            "Benzil Parabeno",
            "Butil Parabeno",
            "Etil Parabeno",
            "Metil Parabeno",
            "Propil Parabeno"
        ]

        for w in custom_words:
            spell.word_frequency.add(w.lower())

        words = text.split()
        corrected_words = []
        for w in words:
            if len(w) > 3 and w.lower() not in spell:
                corr = spell.correction(w)
                corrected_words.append(corr if corr else w)
            else:
                corrected_words.append(w)

        return ' '.join(corrected_words)
