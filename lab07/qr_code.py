import segno
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qrcode_uri = None
    message = None

    if request.method == 'POST':
        message = request.form['data']
        # Generate the QR code object
        qr = segno.make(message)
        # Use the data URI to display it directly in HTML
        qrcode_uri = qr.svg_data_uri(dark = 'darkblue', scale=4)

    # Render the template with optional QR code and message
    return render_template('index.html', qrcode_uri=qrcode_uri, message=message)

if __name__ == '__main__':
    """After running, open link: http://127.0.0.1:5000"""

    app.run(debug=True)

