from sqlalchemy import Date, Boolean, DateTime, Integer, String
from sqlalchemy import ForeignKey, CheckConstraint, or_
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.schema import Column
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import bcrypt
from .serializer import Serializer


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class ContoCorrente(db.Model):
    __tablename__ = "conti_correnti"

    id = Column('id', Integer, primary_key=True)
    saldo = Column('saldo', Integer, CheckConstraint('saldo >= 0'), default=0)
    client1_id = Column(
        'cliente1_id', Integer, ForeignKey("clienti.id")
    )
    client2_id = Column(
        'cliente2_id', Integer, ForeignKey("clienti.id"), nullable=True
    )

    client1 = relationship('Cliente', foreign_keys=[client1_id], lazy=True)
    client2 = relationship('Cliente', foreign_keys=[client2_id], lazy=True)

    def __repr__(self):
        return f"<ContoCorrente {self.id}>"

    # if client2_id is not null, should be different from client1_id
    CheckConstraint('client2_id IS NULL OR client1_id != client2_id',
                    name='check_conto_corrente_clienti')


class Cliente(db.Model, Serializer):
    __tablename__ = "clienti"

    id = Column('id', Integer, primary_key=True)
    email = Column('email', String(length=32), unique=True)
    password = Column('password', String(length=120))
    codice_fiscale = Column('codice_fiscale', String(length=16), unique=True)
    nome = Column('nome', String(length=32))
    cognome = Column('cognome', String(length=32))
    data_nascita = Column('data_nascita', Date())
    indirizzo = Column('indirizzo', String(length=64))
    telefono = Column('telefono', String(length=16))
    bancario_id = Column('bancario_id', Integer, ForeignKey("bancari.id"), nullable=True)

    prestiti = relationship('Prestito', lazy=True, back_populates="cliente")
    mutui = relationship('Mutuo', lazy=True, back_populates="cliente")
    conti_correnti = relationship(
        'ContoCorrente', primaryjoin=or_(ContoCorrente.client1_id == id, ContoCorrente.client2_id == id), lazy=True
    )
    richieste_conti_correnti = relationship('RichiestaContoCorrente', lazy=True, back_populates="cliente")
    bancario = relationship('Bancario', lazy=True, back_populates="clienti")

    def __repr__(self):
        return f"<Cliente {self.id}>"

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
        self.password = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).hex()


class Mutuo(db.Model):
    __tablename__ = "mutui"

    id = Column('id', Integer, primary_key=True)
    importo = Column('importo', Integer, CheckConstraint('importo > 0'))
    data_creazione = Column('data_creazione', DateTime, default=db.func.now())
    data_accettazione = Column('data_accettazione', DateTime, nullable=True)
    accettata = Column('accettata', Boolean, default=False, nullable=True)
    cliente_id = Column('cliente_id', Integer, ForeignKey(
        "clienti.id"))

    garanzie = relationship('Garanzia', lazy=True)
    cliente = relationship('Cliente', back_populates="mutui", lazy=True)

    # if accettata is true, data_accettazione should not be null
    CheckConstraint(
        'accettata = true AND data_accettazione IS NOT NULL OR accettata = false OR accettata IS NULL', name='check_accettata')

    def __repr__(self):
        return f"<Mutuo {self.id}>"

class Prestito(db.Model):
    __tablename__ = "prestiti"

    id = Column('id', Integer, primary_key=True)
    importo = Column('importo', Integer, CheckConstraint('importo > 0'))
    data_creazione = Column('data_creazione', DateTime, default=db.func.now())
    data_accettazione = Column('data_accettazione', DateTime, nullable=True)
    accettata = Column('accettata', Boolean, nullable=True)
    cliente_id = Column('cliente_id', Integer, ForeignKey("clienti.id"))

    garanzie = relationship('Garanzia', lazy=True)
    cliente = relationship('Cliente', back_populates="prestiti", lazy=True)

    # if accettata is true, data_accettazione should not be null
    CheckConstraint(
        'accettata = true AND data_accettazione IS NOT NULL OR accettata = false OR accettata IS NULL', name='check_accettata')

    def __repr__(self):
        return f"<Prestito {self.id}>"


class Garanzia(db.Model):
    __tablename__ = "garanzie"

    id = Column('id', Integer, primary_key=True)
    tipologia = Column('tiplogia', String(length=256))
    file = Column('file', String(length=256))
    valutazione = Column('valutazione', Integer)
    prestito_id = Column('prestito_id', Integer, ForeignKey("prestiti.id"), nullable=True)
    mutuo_id = Column('mutuo_id', Integer, ForeignKey("mutui.id"), nullable=True)

    prestito = relationship('Prestito', back_populates="garanzie", lazy=True)
    mutuo = relationship('Mutuo', back_populates="garanzie", lazy=True)

    # check prestito_id or mutuo_id is not null (not both)
    CheckConstraint('(mutuo_id IS NOT NULL AND prestito_id IS NULL) OR (mutuo_id IS NULL AND prestito_id IS NOT NULL))',
                    name='check_garanzia_prestito_mutuo')

    def __repr__(self):
        return f"<Garanzia {self.id}>"

class RichiestaContoCorrente(db.Model):
    __tablename__ = "richieste_conti_correnti"

    id = Column('id', Integer, primary_key=True)
    data_creazione = Column('data_creazione', DateTime, default=db.func.now())
    data_accettazione = Column('data_accettazione', DateTime, nullable=True)
    accettata = Column('accettata', Boolean, nullable=True)
    cliente_id = Column('cliente_id', Integer, ForeignKey("clienti.id"))

    cliente = relationship('Cliente', back_populates="richieste_conti_correnti", lazy=True)

    # if accettata is true, data_accettazione should not be null
    CheckConstraint(
        'accettata = true AND data_accettazione IS NOT NULL OR accettata = false OR accettata IS NULL', name='check_accettata')

    def __repr__(self):
        return f"<RichiestaContoCorrente {self.id}>"
    

class Bancario(db.Model, Serializer):
    __tablename__ = "bancari"

    id = Column('id', Integer, primary_key=True)
    email = Column('email', String(length=32), unique=True)
    password = Column('password', String(length=120))
    codice_fiscale = Column('codice_fiscale', String(length=16), unique=True)
    nome = Column('nome', String(length=32))
    cognome = Column('cognome', String(length=32))
    data_nascita = Column('data_nascita', Date())
    indirizzo = Column('indirizzo', String(length=64))
    telefono = Column('telefono', String(length=16))

    clienti = relationship('Cliente', lazy=True)

    def __repr__(self):
        return f"<Bancario {self.id}>"

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
        self.password = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).hex()
