from flask import Flask, request, jsonify

app = Flask(__name__)

ingredients_list = [
    "farinha de trigo",
    "açúcar",
    "cacau em pó",
    "fermento em pó",
    "ovos",
    "leite",
    "óleo vegetal",
    "essência de baunilha",
    "sal"
]

allergy_items = [
    "farinha de trigo",
    "cacau em pó"
]

def index():
    return "teste"

@app.route('/ingredients', methods=["POST"])
def get_ingredients():
    ingredients_list_checked = check_allergy_items(ingredients_list, allergy_items)
    print(ingredients_list_checked)

    return jsonify({"received": ingredients_list_checked}), 200

def check_allergy_items(ingredients_list, allergy_items):
    for item in ingredients_list:
        if item in allergy_items:
            print(f"Voce é alergico ao item {item}")
        else:
            print("Não há itens alergicos")

if __name__ == "__main__":
    app.run(debug=True)