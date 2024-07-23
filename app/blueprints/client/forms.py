from flask_wtf import FlaskForm
from wtforms import DateField, FieldList, FormField, IntegerField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

class AccountForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    cognome = StringField('Cognome', validators=[DataRequired()])
    email = StringField('Email', render_kw={'disabled':''})
    password = PasswordField('Password')
    codice_fiscale = StringField('Codice Fiscale', validators=[DataRequired(), Length(min=16, max=16)])
    data_nascita = DateField('Data di Nascita', validators=[DataRequired()])
    indirizzo = StringField('Indirizzo', validators=[DataRequired()])
    telefono = StringField('Telefono', validators=[DataRequired()])
    submit = SubmitField('Modifica')
    
class GaranziaForm(FlaskForm):
    tipologia = StringField('Tipologia', validators=[DataRequired()])
    file = FileField('File', validators=[FileRequired(), FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'Solo file pdf e immagini')])
    valutazione = IntegerField('Valutazione', validators=[DataRequired(), NumberRange(min=0)])

class PrestitoForm(FlaskForm):
    importo = IntegerField('Importo', validators=[DataRequired(), NumberRange(min=0, max=10000)])
    garanzie = FieldList(FormField(GaranziaForm), min_entries=1, render_kw={'style':'list-style-type: none;'})
    submit = SubmitField('Richiedi')