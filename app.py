from flask import Flask, jsonify, render_template, request
from PIL import Image
import pytesseract

app = Flask(__name__)

allergy_user_items = [
    "farinha de trigo",
    "cacau em pó"
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=["POST"])
def get_components():

    try:
        components_user_list = request.form.getlist('components[]')
        image_file = request.files.get('image')
        image_text = process_image(image_file)
        print(image_text)
        allergy_list_checked = check_allergy_items(components_user_list, allergy_user_items)

        if allergy_list_checked:
            return jsonify({"Componentes alérgicos": allergy_list_checked}), 200
        else:    
            return jsonify({"Sucesso": "Você não é alérgico a nada!"}), 200
        
    except Exception as error:

        return jsonify({"error": str(error)}), 500

def check_allergy_items(components_user_list, allergy_user_items):
    allergy_items = []
    not_allergy_items = []

    for item in components_user_list:
        if item in allergy_user_items:
            allergy_items.append(item)
        else:
            not_allergy_items.append(item)

    return allergy_items

def process_image(image_file):
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image)
    return text

if __name__ == "__main__":
    app.run(debug=True)