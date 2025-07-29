from PIL import Image as PilImage, ExifTags, ImageFilter, ImageOps
import pytesseract
import pillow_heif
from io import BytesIO
from spellchecker import SpellChecker
import os

pillow_heif.register_heif_opener()

from services.config import configure_tesseract 

configure_tesseract()

class ImageProcessor:
    def __init__(self, image_file, save_path='processed_images/imagem_processada.png'):
        """
        :param image_file: FileStorage do Flask (request.files["image"])
        """
        self.image_file = image_file
    
    def process_image(self):
        try:
            self.image_file.seek(0)
            image = PilImage.open(BytesIO(self.image_file.read()))

            image = self._correct_orientation(image)
            image = image.convert('L')
            image.thumbnail((800, 800))
            image = ImageOps.autocontrast(image)

            threshold = 160
            image = image.point(lambda p: 255 if p > threshold else 0)
            image = image.filter(ImageFilter.SHARPEN)

            # Extrai texto com pytesseract
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(image, lang='por', config=custom_config)

            # Corrige texto extraído
            corrected_text = self._correct_text(text)

            return corrected_text

        except Exception as e:
            return f"[ERRO] Não foi possível processar a imagem: {str(e)}"

    def _correct_orientation(self, image):
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
