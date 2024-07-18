from flask_wtf import FlaskForm
from wtforms import DateField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

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