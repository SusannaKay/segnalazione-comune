from flask import Flask, render_template, request, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

class Segnalazione(FlaskForm):
    tipologia = SelectField('Modulo per la presentazione di:', choices=['Reclamo','Segnalazione','Suggerimento','Apprezzamento'])
    nome = StringField('Nome')
    cognome = StringField('Cognome')
    indirizzo  = StringField('Indirizzo')
    citta = StringField('Città')
    cap = StringField('CAP')
    telefono = StringField ('Telefono')
    cellulare = StringField ('Cell')
    email  = StringField('e-mail / PEC')
    cod_fiscale  = StringField('Codice Fiscale')
    risposta   = SelectField('Desidero ricervere la risposta, in alternativa, per:', choices=['e-mail','PEC', 'posta', 'telefono','di persona' ])
    luogo  = StringField('Luogo (se pertinente)')
    testo   = StringField('Testo')
    data  = DateField('Data')
    submit = SubmitField('Genera PDF')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = Segnalazione()
    if request.method == 'POST' and form.validate_on_submit():
        # Raccoglie i dati dal form
        dati = {
            'tipologia': form.tipologia.data,
            'nome': form.nome.data,
            'cognome': form.cognome.data,
            'indirizzo': form.indirizzo.data,
            'citta': form.citta.data,
            'cap': form.cap.data,
            'telefono': form.telefono.data,
            'cellulare': form.cellulare.data,
            'email': form.email.data,
            'cod_fiscale': form.cod_fiscale.data,
            'risposta': form.risposta.data,
            'luogo': form.luogo.data,
            'testo': form.testo.data,
            'data': form.data.data.strftime('%d/%m/%Y') if form.data.data else ''
        }
        
        # Genera il PDF compilato
        pdf_compilato = compila_pdf(dati)
        
        # Invia il PDF come risposta
        return send_file(
            pdf_compilato,
            as_attachment=True,
            download_name='segnalazione_compilata.pdf',
            mimetype='application/pdf'
        )

    return render_template('index.html', form=form)

def compila_pdf(dati):
    # Percorso del template PDF
    template_path = os.path.join('pdf_template', 'Modulo reclami Roma.pdf')
    
    # Crea un PDF temporaneo con i campi compilati
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    
    # Funzione per spezzare il testo in righe
    def wrap_text(text, width, font_name, font_size):
        can = canvas.Canvas(None)
        can.setFont(font_name, font_size)
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            line = ' '.join(current_line + [word])
            if can.stringWidth(line) <= width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))
        return lines

    # Impostazioni per il testo
    testo = dati['testo'].upper()
    x = 50
    y = 450
    larghezza_max = 500  # Larghezza massima della riga in punti
    interlinea = 21  # Spazio tra le righe in punti

    # Spezza il testo in righe e disegnale
    font_name = "Helvetica"
    font_size = 12
    righe = wrap_text(testo, larghezza_max, font_name, font_size)
    can.setFont(font_name, font_size)
    for riga in righe:
        can.drawString(x, y, riga)
        y -= interlinea  # Sposta il cursore verso il basso per la prossima riga

    # Aggiungi i campi compilati al PDF
    # Nota: le coordinate (x, y) devono essere adattate al tuo modello PDF specifico
    can.drawString(105, 670, f"{dati['nome']}")
    can.drawString(350, 670, f"{dati['cognome']}")
    can.drawString(105, 645, f"{dati['indirizzo']}")
    can.drawString(350, 645, f"{dati['citta']}")
    can.drawString(435, 645, f"{dati['cap']}")
    can.drawString(105, 625, f"{dati['telefono']}")
    can.drawString(230, 625, f"{dati['cellulare']}")
    can.drawString(105, 600, f"{dati['email']}")
    can.drawString(105, 580, f"{dati['cod_fiscale'].upper()}")
    #can.drawString(100, 500, f"{dati['risposta']}")
    can.drawString(165, 490, f"{dati['luogo']}")
    can.drawString(90, 165, f"{dati['data']}")
    
    # Aggiungi una 'X' nel riquadro corrispondente alla risposta selezionata
    risposta = dati['risposta']
    if risposta == 'e-mail':
        can.drawString(57, 537, 'X')
    elif risposta == 'PEC':
        can.drawString(185, 555, 'X')
    elif risposta == 'posta':
        can.drawString(265, 555, 'X')
    elif risposta == 'telefono':
        can.drawString(345, 555, 'X')
    elif risposta == 'di persona':
        can.drawString(425, 555, 'X')

    can.save()
    
    # Sposta il cursore all'inizio del BytesIO
    packet.seek(0)
    
    # Crea un nuovo PDF con i campi compilati
    new_pdf = PdfReader(packet)
    
    # Leggi il modello PDF esistente
    existing_pdf = PdfReader(open(template_path, "rb"))
    output = PdfWriter()
    
    # Aggiungi la pagina del modello esistente
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    
    # Salva il PDF compilato in memoria
    output_stream = io.BytesIO()
    output.write(output_stream)
    output_stream.seek(0)
    
    return output_stream

if __name__ == '__main__':
    app.run(debug=True)