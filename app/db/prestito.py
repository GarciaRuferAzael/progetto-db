from sqlalchemy import Boolean, DateTime, Integer, CheckConstraint, ForeignKey
from sqlalchemy.schema import Column
from sqlalchemy.orm import relationship
from db.cliente import Cliente
from db.serializer import Serializer
from . import db


class Prestito(db.Model, Serializer):
    __tablename__ = "prestiti"

    id = Column('id', Integer, primary_key=True)
    importo = Column('importo', Integer, CheckConstraint('importo > 0'))
    data_creazione = Column('data_creazione', DateTime, default=db.func.now())
    data_accettazione = Column('data_accettazione', DateTime, nullable=True)
    accettata = Column('accettata', Boolean, nullable=True)
    cliente_id = Column('cliente_id', Integer, ForeignKey(f"{Cliente.__tablename__}.id"))
    
    garanzie = relationship('Garanzia', lazy=True)
    cliente = relationship('Cliente', back_populates=__tablename__, lazy=True)

    # if accettata is true, data_accettazione should not be null
    CheckConstraint(
        'accettata = true AND data_accettazione IS NOT NULL OR accettata = false OR accettata IS NULL',
        name='check_accettata'
    )

    def __repr__(self):
        return f"<Prestito {self.id}>"

    def serialize(self):
        return Serializer.serialize(self)
