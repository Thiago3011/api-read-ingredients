from PIL import Image as PilImage, ExifTags, ImageFilter, ImageOps
import pytesseract
import pillow_heif
from io import BytesIO


pillow_heif.register_heif_opener()

from services.config import configure_tesseract 

configure_tesseract()

class ImageProcessor:
    """
    Classe para processar imagens e extrair texto usando OCR (pytesseract).
    Aplica correções de orientação, ajustes de contraste e nitidez para melhorar o resultado.
    """

    def __init__(self, image_file):
        """
        Inicializa o processador com o arquivo enviado pelo usuário.

        :param image_file: objeto FileStorage recebido pelo Flask (request.files["image"])
        """
        self.image_file = image_file
    
    def process_image(self):
        """
        Abre a imagem, corrige a orientação com base no EXIF, converte para escala de cinza,
        redimensiona, aplica contraste e nitidez, e realiza OCR para extrair texto.

        :return: texto extraído da imagem
        """
        try:
            # Lê os bytes crus do arquivo
            self.image_file.seek(0)
            image = PilImage.open(BytesIO(self.image_file.read()))

            # Corrige orientação com base nos dados EXIF
            image = self._correct_orientation(image)

            # Converte para escala de cinza (L)
            image = image.convert('L')

            # Reduz o tamanho da imagem para no máximo 800x800 pixels, mantendo proporção
            image.thumbnail((800, 800))

            # Ajusta contraste automaticamente para melhorar o OCR
            image = ImageOps.autocontrast(image)

            threshold = 160
            image = image.point(lambda p: 255 if p > threshold else 0)

            # Aplica filtro de nitidez para melhorar definição das letras
            image = image.filter(ImageFilter.SHARPEN)

            # Usa pytesseract para extrair texto da imagem processada
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(image, lang='por', config=custom_config)

            return text

        except Exception as e:
            return f"[ERRO] Não foi possível processar a imagem: {str(e)}"

    def _correct_orientation(self, image):
        """
        Método interno para corrigir a orientação da imagem com base na tag EXIF 'Orientation'.

        :param image: objeto PIL Image
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
        return image  # <--- IMPORTANTE retornar a imagem corrigida
