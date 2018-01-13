from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __repr__(self):
        return "<Item(name='{}')>".format(self.name)
