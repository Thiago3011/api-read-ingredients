from PIL import Image as PilImage, ExifTags, ImageFilter, ImageOps
import pytesseract
import pillow_heif
pillow_heif.register_heif_opener()

class ImageProcessor:
    """
    Classe para processar imagens e extrair texto usando OCR (pytesseract).
    Aplica correções de orientação, ajustes de contraste e nitidez para melhorar o resultado.
    """

    def __init__(self, image_file):
        """
        Inicializa o processador com o caminho do arquivo de imagem.

        :param image_file: caminho para o arquivo de imagem
        """
        self.image_file = image_file
    
    def process_image(self):
        """
        Abre a imagem, corrige a orientação com base no EXIF, converte para escala de cinza,
        redimensiona, aplica contraste e nitidez, e realiza OCR para extrair texto.

        :return: texto extraído da imagem
        """
        # Abre a imagem usando PIL
        image = PilImage.open(self.image_file)

        # Corrige orientação com base nos dados EXIF
        self._correct_orientation(image)

        # Converte para escala de cinza (L)
        image = image.convert('L')

        # Reduz o tamanho da imagem para no máximo 800x800 pixels, mantendo proporção
        image.thumbnail((800, 800))

        # Ajusta contraste automaticamente para melhorar o OCR
        image = ImageOps.autocontrast(image)

        # Aplica filtro de nitidez para melhorar definição das letras
        image = image.filter(ImageFilter.SHARPEN)

        # Usa pytesseract para extrair texto da imagem processada
        text = pytesseract.image_to_string(image)

        return text

    def _correct_orientation(self, image):
        """
        Método interno para corrigir a orientação da imagem com base na tag EXIF 'Orientation'.

        :param image: objeto PIL Image
        """
        try:
            # Busca o código da tag 'Orientation' no dicionário EXIF
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break

            exif = image._getexif()
            if exif is not None:
                orientation_value = exif.get(orientation, None)

                # Rotaciona a imagem conforme valor da orientação EXIF
                if orientation_value == 3:
                    image.rotate(180, expand=True)
                elif orientation_value == 6:
                    image.rotate(270, expand=True)
                elif orientation_value == 8:
                    image.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # Se imagem não tem dados EXIF ou tag Orientation, ignora
            pass
