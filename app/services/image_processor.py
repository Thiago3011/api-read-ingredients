from io import BytesIO

from PIL import Image as PilImage, ExifTags, ImageFilter, ImageOps
import pillow_heif
import pytesseract
from spellchecker import SpellChecker

from app.core.config import settings

if settings.TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD

pillow_heif.register_heif_opener()


class ImageProcessor:
    def __init__(self, image_file):
        self.image_file = image_file
        
    def process_image(self):
        """
        Processa a imagem e retorna o texto extraído pelo OCR.
        """
        try:
            self.image_file.seek(0)

            image = PilImage.open(
                BytesIO(self.image_file.read())
            )

            image = self._correct_orientation(image)
            image = image.convert("L")
            image.thumbnail((800, 800))
            image = ImageOps.autocontrast(image)

            threshold = 160
            image = image.point(
                lambda p: 255 if p > threshold else 0
            )

            image = image.filter(ImageFilter.SHARPEN)

            custom_config = r"--oem 3 --psm 6"

            text = pytesseract.image_to_string(
                image,
                lang="por",
                config=custom_config
            )

            return self._correct_text(text)

        except Exception as e:
            return f"[ERRO] Não foi possível processar a imagem: {str(e)}"
    
    def _correct_orientation(self, image):
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == "Orientation":
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
        Corrige o texto extraído pelo OCR utilizando o SpellChecker.
        """

        spell = SpellChecker(language="pt")

        words = text.split()
        corrected_words = []

        for word in words:
            if len(word) > 3 and word.lower() not in spell:
                correction = spell.correction(word)
                corrected_words.append(
                    correction if correction else word
                )
            else:
                corrected_words.append(word)

        return " ".join(corrected_words)