from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets import DateInput

class SegnalazioneForm(FlaskForm):
    tipologia = SelectField('Tipologia', choices=[
        ('Reclamo', 'Reclamo'),
        ('Segnalazione', 'Segnalazione'),
        ('Suggerimento', 'Suggerimento'),
        ('Apprezzamento', 'Apprezzamento')
    ], validators=[DataRequired()])
    
    nome = StringField('Nome', validators=[DataRequired(), Length(max=50)])
    cognome = StringField('Cognome', validators=[DataRequired(), Length(max=50)])
    indirizzo = StringField('Indirizzo', validators=[DataRequired(), Length(max=100)])
    citta = StringField('Città', validators=[DataRequired(), Length(max=50)])
    cap = StringField('CAP', validators=[DataRequired(), Length(5, 5)])
    telefono = StringField('Telefono', validators=[Length(max=20)])
    cellulare = StringField('Cellulare', validators=[Length(max=20),DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    pec = StringField('PEC', validators=[Email()])
    cod_fiscale = StringField('Codice Fiscale', validators=[DataRequired(), Length(16, 16)])
    
    risposta = SelectField('Risposta', choices=[
        ('e-mail', 'E-mail'),
        ('PEC', 'PEC'),
        ('posta', 'Posta'),
        ('telefono', 'Telefono'),
        ('di persona', 'Di persona')
    ], validators=[DataRequired()])
    
    luogo = StringField('Luogo', validators=[DataRequired(), Length(max=100)])
    testo = TextAreaField('Testo della segnalazione', validators=[DataRequired()])
    data = DateField('Data', format='%d-%m-%Y', validators=[DataRequired()], 
                     render_kw={"type": "date", "pattern": r"\d{2}-\d{2}-\d{4}"})
