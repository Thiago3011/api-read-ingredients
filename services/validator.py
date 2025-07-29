class ComponentsValidator:
    def __init__(self, user_components, image_text=""):
        self.user_components = user_components
        self.image_text = image_text

    def check_allergy_items(self):

        allergy_user_items = [
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

        result_of_allergy_items = []

        for alergia in self.user_components:
            if alergia.lower() in allergy_user_items:
                result_of_allergy_items.append(alergia)

        if self.image_text:
            for alergia in allergy_user_items:
                if alergia.lower() in self.image_text and alergia not in result_of_allergy_items:
                    result_of_allergy_items.append(alergia)

        return result_of_allergy_items