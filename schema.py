from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import ForeignKey, desc
from sqlalchemy.orm import relationship

Base = declarative_base()


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    image_filename = Column(String)
    is_place = Column(Boolean)

    created = Column(DateTime)
    updated = Column(DateTime)

    def __repr__(self):
        return "<Item(name='{}')>".format(self.name)


class Position(Base):
    __tablename__ = 'position'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    datetime = Column(DateTime)

    created = Column(DateTime)
    updated = Column(DateTime)

    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship(
        'Item',
        back_populates='positions',
        foreign_keys='Position.item_id',
    )

    place_id = Column(Integer, ForeignKey('item.id'))
    place = relationship(
        'Item',
        back_populates='reverse_positions',
        foreign_keys='Position.place_id',
    )

    def __repr__(self):
        return "<Position(item.name='{}', name='{}', datetime={}>".format(self.item.name, self.name, self.datetime)


Item.positions = relationship(
    "Position", order_by=desc(Position.datetime), back_populates="item",
    foreign_keys='Position.item_id',
)

Item.reverse_positions = relationship(
    "Position", order_by=desc(Position.datetime), back_populates="place",
    foreign_keys='Position.place_id',
)
