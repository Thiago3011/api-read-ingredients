from flask import Flask, request, jsonify

app = Flask(__name__)

ingredients_user_list = [
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

allergy_user_items = [
    "farinha de trigo",
    "cacau em pó"
]

@app.route('/')
def index():
    return "teste"

@app.route('/ingredients', methods=["POST"])
def get_ingredients():
    allergy_list_checked, ingredients_list_checked = check_allergy_items(ingredients_user_list, allergy_user_items)

    return jsonify({"allergy_items": allergy_list_checked}, {"ingredients_list_checked": ingredients_list_checked}), 200

def check_allergy_items(ingredients_user_list, allergy_user_items):
    allergy_items = []
    not_allergy_items = []

    for item in ingredients_user_list:
        if item in allergy_user_items:
            allergy_items.append(item)
        else:
            not_allergy_items.append(item)

    return allergy_items, not_allergy_items

if __name__ == "__main__":
    app.run(debug=True)