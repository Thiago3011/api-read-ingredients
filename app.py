from flask import Flask, jsonify, render_template, request
from PIL import Image, ExifTags, ImageFilter, ImageOps
import pytesseract
import platform
import pillow_heif
pillow_heif.register_heif_opener()

if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
else:
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

app = Flask(__name__)

allergy_user_items = [
    "farinha de trigo",
    "cacau em pó",
    "bracelete",
    "AQUA",
    "GLYCERIN"
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=["POST"])
def get_components():

    try:
        components_user_list = request.form.getlist('components[]')
        image_file = request.files.get('image')

        if not image_file or image_file.filename == '':
            return jsonify({'error': 'Arquivo não enviado corretamente'})
        
        if image_file:
            image_text = process_image(image_file).lower()
            allergy_list_checked = check_allergy_items(components_user_list, allergy_user_items, image_text)
        else:
            allergy_list_checked = check_allergy_items(components_user_list, allergy_user_items)

        if allergy_list_checked:
            return jsonify({"Componentes alérgicos": allergy_list_checked}), 200
        else:    
            return jsonify({"Sucesso": "Você não é alérgico a nada!"}), 200
        
    except Exception as error:

        return jsonify({"error": str(error)}), 500

def check_allergy_items(components_user_list, allergy_user_items, image_text=""):
    allergy_items = []

    for item in components_user_list:
        if item in allergy_user_items:
            allergy_items.append(item)

    if image_text:
        for alergia in allergy_user_items:
            if alergia.lower() in image_text and alergia not in allergy_items:
                allergy_items.append(alergia)

    return allergy_items

def process_image(image_file):
    image = Image.open(image_file)

    # Corrige a orientação EXIF
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
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
        # imagem sem EXIF
        pass

    image = image.convert('L')

    # Reduz tamanho para evitar lentidão e melhorar OCR
    image.thumbnail((1024, 1024))
    
    # Aumenta contraste
    image = ImageOps.autocontrast(image)

    # Aplica filtro de nitidez para melhorar as bordas das letras
    image = image.filter(ImageFilter.SHARPEN)


    text = pytesseract.image_to_string(image)
    return text

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
