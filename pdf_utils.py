import io
import os
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
from datetime import datetime

def compila_pdf(dati):
    # Stampa di debug
    print("Dati ricevuti in compila_pdf:", dati)

    # Percorso del template PDF
    template_path = os.path.join('pdf_template', 'Modulo reclami Roma.pdf')
    
    # Crea un PDF temporaneo con i campi compilati
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    
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

    # Prima pagina
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
    can.drawString(105, 670, f"{dati['nome']}")
    can.drawString(350, 670, f"{dati['cognome']}")
    can.drawString(105, 645, f"{dati['indirizzo']}")
    can.drawString(350, 645, f"{dati['citta']}")
    can.drawString(435, 645, f"{dati['cap']}")
    can.drawString(105, 625, f"{dati['telefono']}")
    can.drawString(230, 625, f"{dati['cellulare']}")
    can.drawString(105, 600, f"{dati['email']}")
    can.drawString(330, 600, f"{dati['pec']}")
    can.drawString(105, 580, f"{dati['cod_fiscale'].upper()}")
    can.drawString(165, 490, f"{dati['luogo']}")
    
    # Modifica questa riga
    data_formattata = datetime.strptime(dati['data'], '%Y-%m-%d').strftime('%d-%m-%Y')
    can.drawString(90, 165, data_formattata)
    
    # Aggiungi una 'X' nel riquadro corrispondente alla risposta selezionata
    risposta = dati['risposta']
    if risposta == 'e-mail':
        can.drawString(57, 537, 'X')
    elif risposta == 'PEC':
        can.drawString(110, 537, 'X')
    elif risposta == 'posta':
        can.drawString(165, 537, 'X')
    elif risposta == 'telefono':
        can.drawString(210, 537, 'X')
    elif risposta == 'di persona':
        can.drawString(270, 537, 'X')
    
    tipologia = dati['tipologia']
    if tipologia == 'Reclamo':
        can.drawString(87, 701, 'X')
    elif tipologia == 'Segnalazione':
        can.drawString(170, 701, 'X')
    elif tipologia == 'Suggerimento':
        can.drawString(273, 701, 'X')
    elif tipologia == 'Apprezzamento':
        can.drawString(377, 701, 'X')

    # Aggiungi la firma se presente
    if dati['signature'] is not None:
        try:
            signature_image = Image.open(io.BytesIO(dati['signature']))
            signature_image = signature_image.convert('RGB')
            signature_image = signature_image.resize((200, 100), Image.LANCZOS)
            can.drawInlineImage(signature_image, 300, 90, width=200, height=100)
            print("Firma aggiunta al PDF")
        except Exception as e:
            print(f"Errore nell'aggiunta della firma: {str(e)}")
    else:
        print("Nessuna firma da aggiungere")

    # Seconda pagina (se necessario)
    can.showPage()
    # Aggiungi qui i campi per la seconda pagina, se ce ne sono

    # Terza pagina (se necessario)
    can.showPage()
    # Aggiungi qui i campi per la terza pagina, se ce ne sono

    can.save()

    # Unisci il template con i dati compilati
    packet.seek(0)
    new_pdf = PdfReader(packet)
    existing_pdf = PdfReader(open(template_path, "rb"))
    output = PdfWriter()

    # Unisci tutte le pagine
    for i in range(len(existing_pdf.pages)):
        page = existing_pdf.pages[i]
        if i < len(new_pdf.pages):
            page.merge_page(new_pdf.pages[i])
        output.add_page(page)

    output_stream = io.BytesIO()
    output.write(output_stream)
    output_stream.seek(0)

    return output_stream
