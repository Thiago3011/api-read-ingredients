from app.database import SessionLocal
from app.models.allergy import Allergy


ALLERGIES = [
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
    "Propil Parabeno",
]


def seed_allergies():
    db = SessionLocal()

    try:
        for name in ALLERGIES:
            allergy = Allergy(name=name)
            db.add(allergy)

        db.commit()

        print(f"{len(ALLERGIES)} alergias cadastradas!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_allergies()