from datetime import datetime
from random import randrange
from sqlalchemy import Date, Boolean, DateTime, Integer, String, UniqueConstraint
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


class Filiale(db.Model):
    __tablename__ = "filiali"

    id = Column('id', Integer, primary_key=True)
    saldo = Column('saldo', Integer, CheckConstraint('saldo >= 0'), default=0)
    sede = Column('sede', String(length=64))

    bancari = relationship('Bancario', lazy=True)
    conti_correnti = relationship('ContoCorrente', lazy=True)
    storico_direzioni = relationship(
        'StoricoDirezione', back_populates='filiale', lazy=True)

    def __repr__(self):
        return f"<Filiale {self.id}>"

    @property
    def direttore(self):
        """
        Direttore assigned to Filiale for the current year
        """
        current_year = datetime.now().year
        current_storico = (db.session.query(StoricoDirezione)
                           .filter_by(filiale_id=self.id, year=current_year)
                           .first())
        return current_storico.direttore if current_storico else None


class ContoCorrente(db.Model):
    __tablename__ = "conti_correnti"

    id = Column('id', Integer, primary_key=True)
    saldo = Column('saldo', Integer, CheckConstraint('saldo >= 0'), default=0)
    iban = Column('iban', String(length=27), unique=True)
    cliente1_id = Column(
        'cliente1_id', Integer, ForeignKey("clienti.id")
    )
    cliente2_id = Column(
        'cliente2_id', Integer, ForeignKey("clienti.id"), nullable=True
    )
    filiale_id = Column('filiale_id', Integer, ForeignKey("filiali.id"))

    cliente1 = relationship('Cliente', foreign_keys=[
        cliente1_id], back_populates='conti_correnti', lazy=True)
    cliente2 = relationship('Cliente', foreign_keys=[
        cliente2_id], back_populates='conti_correnti', lazy=True)
    filiale = relationship(
        'Filiale', back_populates='conti_correnti', lazy=True)

    def __repr__(self):
        return f"<ContoCorrente {self.id}>"

    # if cliente2_id is not null, should be different from cliente1_id
    CheckConstraint('cliente2_id IS NULL OR cliente1_id != cliente2_id',
                    name='check_conto_corrente_clienti')
    
    # unique iban
    UniqueConstraint('iban', name='unique_iban')

    def generate_iban(self):
        country_code = 'IT'
        checksum = '00'  # Placeholder for checksum
        bban = f'{self.filiale_id}{randrange(1000, 10000)}{self.cliente1_id:012d}'
        temp_iban = f'{country_code}{checksum}{bban}'

        # Calculate the checksum
        numeric_iban = ''.join(str(int(ch, 36)) for ch in temp_iban)
        checksum = 98 - (int(numeric_iban) % 97)
        self.iban = f'{country_code}{checksum:02d}{bban}'


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
    bancario_id = Column('bancario_id', Integer,
                         ForeignKey("bancari.id"), nullable=True)

    prestiti = relationship('Prestito', lazy=True, back_populates="cliente")
    mutui = relationship('Mutuo', lazy=True, back_populates="cliente")
    conti_correnti = relationship(
        'ContoCorrente', primaryjoin=or_(ContoCorrente.cliente1_id == id, ContoCorrente.cliente2_id == id), lazy=True, viewonly=True
    )
    richieste_conti_correnti = relationship(
        'RichiestaContoCorrente', lazy=True, back_populates="cliente")
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
    prestito_id = Column('prestito_id', Integer,
                         ForeignKey("prestiti.id"), nullable=True)
    mutuo_id = Column('mutuo_id', Integer,
                      ForeignKey("mutui.id"), nullable=True)

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
    bancario_id = Column('bancario_id', Integer, ForeignKey("bancari.id"))

    cliente = relationship(
        'Cliente', back_populates="richieste_conti_correnti", lazy=True)
    bancario = relationship(
        'Bancario', back_populates="richieste_conti_correnti", lazy=True)

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
    filiale_id = Column('filiale_id', Integer, ForeignKey("filiali.id"))

    clienti = relationship('Cliente', lazy=True)
    filiale = relationship('Filiale', back_populates='bancari', lazy=True)
    richieste_conti_correnti = relationship(
        'RichiestaContoCorrente', lazy=True)

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


class Direttore(db.Model, Serializer):
    __tablename__ = "direttori"

    id = Column('id', Integer, primary_key=True)
    email = Column('email', String(length=32), unique=True)
    password = Column('password', String(length=120))
    codice_fiscale = Column('codice_fiscale', String(length=16), unique=True)
    nome = Column('nome', String(length=32))
    cognome = Column('cognome', String(length=32))
    data_nascita = Column('data_nascita', Date())
    indirizzo = Column('indirizzo', String(length=64))
    telefono = Column('telefono', String(length=16))

    storico_direzioni = relationship(
        'StoricoDirezione', back_populates='direttore', lazy=True)

    def __repr__(self):
        return f"<Direttore {self.id}>"

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

    @property
    def filiale(self):
        """
        Filiale assigned to Direttore for the current year
        """
        current_year = datetime.now().year
        current_storico = (db.session.query(StoricoDirezione)
                           .filter_by(direttore_id=self.id, year=current_year)
                           .first())
        return current_storico.filiale if current_storico else None


class StoricoDirezione(db.Model):
    __tablename__ = "storico_direzione"

    id = Column('id', Integer, primary_key=True)
    year = Column('year', Integer)
    direttore_id = Column('direttore_id', Integer, ForeignKey("direttori.id"))
    filiale_id = Column('filiale_id', Integer, ForeignKey("filiali.id"))

    direttore = relationship('Direttore', back_populates='storico_direzioni')
    filiale = relationship('Filiale', back_populates='storico_direzioni')

    UniqueConstraint('year', 'direttore_id', 'filiale_id',
                     name='unique_direttore_filiale_year')


class TransazioneInterna(db.Model):
    __tablename__ = "transazioni_interne"

    id = Column('id', Integer, primary_key=True)
    conto_corrente_id = Column(
        'conto_corrente_id', Integer, ForeignKey("conti_correnti.id"))

    conto_corrente = relationship('ContoCorrente', lazy=True)

    def __repr__(self):
        return f"<TransazioneInterna {self.id}>"


class TransazioneEsterna(db.Model):
    __tablename__ = "transazioni_esterne"

    id = Column('id', Integer, primary_key=True)
    iban = Column('iban', String(length=27))

    def __repr__(self):
        return f"<TransazioneEsterna {self.id}>"


class Transazione(db.Model):
    __tablename__ = "transazioni"

    id = Column('id', Integer, primary_key=True)
    importo = Column('importo', Integer, CheckConstraint('importo > 0'))
    data = Column('data', DateTime, default=db.func.now())
    entrata = Column('entrata', Boolean, default=False)
    descrizione = Column('descrizione', String(length=256))
    causale = Column('causale', String(length=256), nullable=True)
    transazione_interna_id = Column('transazione_interna_id', Integer, ForeignKey(
        "transazioni_interne.id"), nullable=True)
    transazione_esterna_id = Column('transazione_esterna_id', Integer, ForeignKey(
        "transazioni_esterne.id"), nullable=True)
    # a Transazione can make reference to another Transazione
    transazione_id = Column('transazione_id', Integer, ForeignKey('transazioni.id'), nullable=True)

    transazione_interna = relationship(
        'TransazioneInterna', backref='transazione', uselist=False, lazy=True)
    transazione_esterna = relationship(
        'TransazioneEsterna', backref='transazione', uselist=False, lazy=True)
    transazione = relationship(
        'Transazione', remote_side=[id], uselist=False, lazy=True)
    
    # check transazione_esterna_id or transazione_interna_id is not null (not both)
    CheckConstraint(
        '(transazione_interna_id IS NOT NULL AND transazione_esterna_id IS NULL) OR (transazione_interna_id IS NULL AND transazione_esterna_id IS NOT NULL))'
    )
    # check transazione_id is not equal to id
    CheckConstraint(
        'transazione_id IS NULL OR transazione_id != id'
    )

    def __repr__(self):
        return f"<Transazione {self.id}>"