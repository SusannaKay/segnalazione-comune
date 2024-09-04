from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
from forms import SegnalazioneForm
from pdf_utils import compila_pdf
from flask_bootstrap import Bootstrap5
import io
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'una_chiave_segreta_molto_lunga_e_complessa'
   
bootstrap = Bootstrap5(app)
@app.route('/', methods=['GET', 'POST'])
def index():
    form = SegnalazioneForm()
    if form.validate_on_submit():
        return redirect(url_for('preview_pdf'))
    return render_template('index.html', form=form)

@app.route('/preview_pdf', methods=['POST'])
def preview_pdf():
    try:
        form_data = request.form.to_dict()
        signature_data = form_data.get('signature')
        app.logger.info(f"Lunghezza dati firma ricevuti: {len(signature_data) if signature_data else 'Nessun dato'}")
        
        # Se la firma è presente, convertiamo i dati base64 in bytes
        if signature_data and signature_data.startswith('data:image/png;base64,'):
            signature_data = signature_data.split(',')[1]
            form_data['signature'] = base64.b64decode(signature_data)
        else:
            form_data['signature'] = None
        
        pdf_stream = compila_pdf(form_data)
        return send_file(
            pdf_stream,
            as_attachment=True,
            download_name='segnalazione.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        app.logger.error(f"Errore durante la generazione del PDF: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)