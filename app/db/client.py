import bcrypt
from sqlalchemy import Date, Integer, String
from sqlalchemy.schema import Column

from db.serializer import Serializer
from . import db

class Client(db.Model, Serializer):
    __tablename__ = "clienti"
     
    id = Column('id', Integer, primary_key=True)
    email = Column('email', String(length=32), unique=True)
    password = Column('password', String(length=120))
    codice_fiscale = Column('codice_fiscale', String(length=16), unique=True)
    nome = Column('name', String(length=32))
    cognome = Column('cognome', String(length=32))
    data_nascita = Column('data_nascita', Date())
    indirizzo = Column('indirizzo', String(length=64))
    telefono = Column('telefono', String(length=16))
    
    def __repr__(self):
        return f"<Client {self.id}>"
    
        
    def serialize(self):
        d = Serializer.serialize(self)
        del d['password']
        return d
    
    def verify_password(self, password: str):
        return bcrypt.checkpw(
            password.encode(),
            bytes.fromhex(self.__getattribute__('password'))
        )
    
    def set_password(self, password: str):
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).hex()