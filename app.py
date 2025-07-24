from flask import Flask, jsonify, render_template, request

from services.image_processor import ImageProcessor
from services.validator import ComponentsValidator

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=["POST"])
def get_components():

    try:
        components_user_list = request.form.getlist('components[]')
        image_file = request.files.get('image')

        if image_file and image_file.filename:

            logger.info(f"📷 Nome do arquivo: {image_file.filename}")
            logger.info(f"📦 Tipo MIME: {image_file.content_type}")
            image_file.stream.seek(0)  # volta para o início do arquivo, para garantir leitura correta

            image_processor = ImageProcessor(image_file)
            image_text = image_processor.process_image().lower()

            logger.info(f"Texto extraído da imagem (preview): {image_text[:100]}")


            if not image_text or '[ERRO]' in image_text:
                return jsonify({"error": "Não foi possível processar a imagem ou extrair texto."}), 400

            components_validator = ComponentsValidator(components_user_list, image_text)
            allergy_list_checked = components_validator.check_allergy_items()
        else:
            components_validator = ComponentsValidator(components_user_list)
            allergy_list_checked = components_validator.check_allergy_items()

        if allergy_list_checked:
            return jsonify({"Componentes alérgicos": allergy_list_checked}), 200
        else:    
            return jsonify({"Sucesso": "Você não é alérgico a nada!"}), 200
        
    except Exception as error:
        logger.error(f"Erro no processamento: {error}", exc_info=True)

        return jsonify({"error": str(error)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# if __name__ == "__main__":
#     app.run(debug=True)
