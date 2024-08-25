from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

class Segnalazione(FlaskForm):
    tipologia = SelectField('Modulo per la presentazione di:', choices=['Reclamo','Segnalazione','Suggerimento','Apprezzamento'])
    nome = StringField('Nome')
    cognome = StringField('Cognome')
    indirizzo  = StringField('Indirizzo')
    citta = StringField('Città')
    cap = IntegerField('CAP')
    telefono = IntegerField ('Telefono')
    cellulare = IntegerField ('Cell')
    email  = StringField('e-mail / PEC')
    cod_fiscale  = StringField('Codice Fiscale')
    risposta   = SelectField('Desidero ricervere la risposta, in alternativa, per:', choices=['e-mail','PEC', 'posta', 'telefono','di persona' ])
    luogo  = StringField('Luogo (se pertinente)')
    testo   = StringField('Testo')
    data  = DateField('Data')
    submit = SubmitField('Genera PDF')


@app.route('/')
def home():
    form = Segnalazione()
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)