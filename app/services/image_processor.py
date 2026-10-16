from io import BytesIO
import logging
from time import perf_counter

from PIL import Image as PilImage, ExifTags, ImageFilter, ImageOps
import pillow_heif
import pytesseract
from spellchecker import SpellChecker

from app.core.config import settings

if settings.TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD

pillow_heif.register_heif_opener()

# Load the Portuguese dictionary once per process, not for every image.
SPELL_CHECKER = SpellChecker(language="pt")
logger = logging.getLogger(__name__)


class ImageProcessor:
    def __init__(self, image_file):
        self.image_file = image_file
        
    def process_image(self):
        """
        Processa a imagem e registra o tempo de cada etapa para diagnóstico.
        """
        total_started = perf_counter()

        try:
            self.image_file.seek(0)

            preprocessing_started = perf_counter()
            image = PilImage.open(
                BytesIO(self.image_file.read())
            )
            image = self._correct_orientation(image)
            original_width, original_height = image.size

            image = image.convert("L")
            image.thumbnail((800, 800))
            image = ImageOps.autocontrast(image)

            threshold = 160
            image = image.point(
                lambda p: 255 if p > threshold else 0
            )
            image = image.filter(ImageFilter.SHARPEN)

            processed_width, processed_height = image.size
            preprocessing_seconds = perf_counter() - preprocessing_started

            custom_config = r"--oem 3 --psm 6"
            ocr_started = perf_counter()
            text = pytesseract.image_to_string(
                image,
                lang="por",
                config=custom_config
            )
            tesseract_seconds = perf_counter() - ocr_started

            spellcheck_started = perf_counter()
            corrected_text = self._correct_text(text)
            spellcheck_seconds = perf_counter() - spellcheck_started
            total_seconds = perf_counter() - total_started

            # Timing and dimensions only: do not log label contents.
            logger.info(
                "OCR timing: preprocess=%.3fs tesseract=%.3fs "
                "spellcheck=%.3fs total=%.3fs "
                "image=%sx%s processed=%sx%s words=%s",
                preprocessing_seconds,
                tesseract_seconds,
                spellcheck_seconds,
                total_seconds,
                original_width,
                original_height,
                processed_width,
                processed_height,
                len(text.split()),
            )

            return corrected_text

        except Exception as e:
            logger.exception(
                "Image processing failed after %.3fs",
                perf_counter() - total_started,
            )
            raise ValueError(
                f"Não foi possível processar a imagem: {str(e)}"
            ) from e
    
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

        words = text.split()
        corrected_words = []

        for word in words:
            if len(word) > 3 and word.lower() not in SPELL_CHECKER:
                correction = SPELL_CHECKER.correction(word)
                corrected_words.append(
                    correction if correction else word
                )
            else:
                corrected_words.append(word)

        return " ".join(corrected_words)