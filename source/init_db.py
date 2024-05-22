from sqlalchemy.orm import sessionmaker
from bank import Base
from sqlalchemy import engine, create_engine

# Créer une connexion
def setup_db(url='sqlite:///bank.db'):
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()

# engine = create_engine('sqlite:///bank.db')
# Base.metadata.create_all(engine)

# # conn = engine.connect()

# # Créer une session
# Session = sessionmaker(bind=engine)
# session = Session()


if __name__ == '__main__':
    # Créer les tables
    setup_db()
  



