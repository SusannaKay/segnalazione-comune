var signaturePad;

function resizeCanvas() {
    var ratio = Math.max(window.devicePixelRatio || 1, 1);
    var canvas = document.querySelector("#signature-pad canvas");
    canvas.width = canvas.offsetWidth * ratio;
    canvas.height = canvas.offsetHeight * ratio;
    canvas.getContext("2d").scale(ratio, ratio);
    if (signaturePad) {
        signaturePad.clear(); // Pulisce la firma esistente
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var canvas = document.querySelector("#signature-pad canvas");
    signaturePad = new SignaturePad(canvas, {
        backgroundColor: 'rgb(255, 255, 255)'
    });

    window.addEventListener("resize", resizeCanvas);
    resizeCanvas();

    document.getElementById('clear-signature').addEventListener('click', function() {
        signaturePad.clear();
    });

    document.getElementById('segnalazioneForm').addEventListener('submit', function(event) {
        event.preventDefault();
        if (signaturePad.isEmpty()) {
            alert("Per favore, firma il documento prima di generare il PDF.");
            return;
        }
        document.getElementById('signature-data').value = signaturePad.toDataURL('image/png');
        console.log("Dati firma:", document.getElementById('signature-data').value);
        this.submit();
    });

    document.getElementById('previewPDF').addEventListener('click', function() {
        if (signaturePad.isEmpty()) {
            alert("Per favore, firma il documento prima di generare l'anteprima.");
            return;
        }
        document.getElementById('signature-data').value = signaturePad.toDataURL();
        var formData = new FormData(document.getElementById('segnalazioneForm'));
        
        fetch('/preview_pdf', {
            method: 'POST',
            body: formData
        })
        .then(response => response.blob())
        .then(blob => {
            var url = URL.createObjectURL(blob);
            window.open(url, '_blank');
        })
        .catch(error => {
            console.error('Errore:', error);
            alert('Si è verificato un errore durante la generazione del PDF. Per favore, riprova.');
        });
    });
});
