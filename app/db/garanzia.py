from sqlalchemy import CheckConstraint, Integer, String, ForeignKey
from sqlalchemy.schema import Column
from sqlalchemy.orm import relationship
from db.serializer import Serializer
from db.prestito import Prestito
from .mutuo import Mutuo
from . import db

class Garanzia(db.Model, Serializer):
    __tablename__ = "garanzie"
     
    id = Column('id', Integer, primary_key=True)
    tipologia = Column('tiplogia', String(length=256))
    file = Column('file', String(length=256))
    valutazione = Column('valutazione', Integer)
    prestito_id = Column('prestito_id', Integer, ForeignKey(f"{Prestito.__tablename__}.id"), nullable=True)
    mutuo_id = Column('mutuo_id',  Integer, ForeignKey(f"{Mutuo.__tablename__}.id"), nullable=True)
    
    prestito = relationship('Prestito', back_populates=__tablename__, lazy=True)
    mutuo = relationship('Mutuo', back_populates=__tablename__, lazy=True)
    
    # check prestito_id or mutuo_id is not null (not both)
    CheckConstraint(
        '(mutuo_id IS NOT NULL AND prestito_id IS NULL) OR (mutuo_id IS NULL AND prestito_id IS NOT NULL))',
        name='check_garanzia_prestito_mutuo'
    )
    
    def __repr__(self):
        return f"<Garanzia {self.id}>"
    
    def serialize(self):
        return Serializer.serialize(self)