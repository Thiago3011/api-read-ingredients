print("1 - iniciando")

from app.database import Base, engine

print("2 - database importado")

from app.models.user import User

print("3 - User importado")

Base.metadata.create_all(bind=engine)

print("4 - tabelas criadas!")