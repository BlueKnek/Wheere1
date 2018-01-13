from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schema import Base

engine = create_engine('sqlite:///db.sqlite3', echo=True)
Session = sessionmaker(bind=engine)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
