"""
    Arquivo principal do aplicação Flask responsável por gerenciar as rotas, chamar os serviços e rodar o servidor.
"""

# importações necessárias para funcionamento do Flask.
from flask import Flask, jsonify, render_template, request

# importações dos serviços utilizados para processar a imagem e validar os componentes.
from services.image_processor import ImageProcessor
from services.validator import ComponentsValidator

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def get_components():

    """
        Rota principal para receber os componentes e imagem do body para realização das validações e tratativas.

        - GET: renderiza a página inicial com o formulário.
        - POST: processa os dados enviados (componentes e/ou imagem), realiza a verificação de alergênicos e exibe os resultados.

        returns:
            - render_template: renderiza o template de resposta da requisição com a lista de alergênicos encontrados.
            - jsonify: JSON de erro com status HTTP apropriado, se necessário.
    """

    if request.method == "POST":
        try:
            components_user_list = request.form.getlist('components[]')
            image_file = request.files.get('image')

            if image_file and image_file.filename:

                image_file.stream.seek(0)  # Garante que a leitura do arquivo comece do início

                image_processor = ImageProcessor(image_file) # instacia o processador de imagem
                image_text = image_processor.process_image().lower() # Extrai texto da imagem

                # Verifica se houve erro no processamento OCR
                if not image_text or '[ERRO]' in image_text:
                    return jsonify({"error": "Não foi possível processar a imagem ou extrair texto."}), 400

                components_validator = ComponentsValidator(components_user_list, image_text) # instacia o validador de componentes
                allergy_list_checked = components_validator.check_allergy_items() # realiza a validação dos componentes
            else:
                components_validator = ComponentsValidator(components_user_list)
                allergy_list_checked = components_validator.check_allergy_items()

            if allergy_list_checked:
                return render_template('result.html', allergy_list=allergy_list_checked) # envia ao frontend a lista de alergênicos encontrados
            else:    
                return render_template('result.html'), 200
            
        except Exception as error:
            return jsonify({"error": str(error)}), 500
        
    else:
        return render_template('index.html')
        
# Executa o servidor localmente
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
