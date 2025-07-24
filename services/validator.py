class ComponentsValidator:
    def __init__(self, user_components, image_text=""):
        self.user_components = user_components
        self.image_text = image_text

    def check_allergy_items(self):

        allergy_user_items = [
            "farinha de trigo",
            "cacau em pó",
            "bracelete",
            "aqua",
            "glycerin"
        ]

        result_of_allergy_items = []

        for alergia in self.user_components:
            if alergia.lower() in allergy_user_items:
                result_of_allergy_items.append(alergia)

        if self.image_text:
            for alergia in allergy_user_items:
                if alergia.lower() in self.image_text and alergia not in result_of_allergy_items:
                    result_of_allergy_items.append(alergia)

        return result_of_allergy_items