from flask import Flask, render_template, request, send_file
import qrcode
from PIL import Image
import io
import base64

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    # Get the URL from the form input
    url = request.form.get('url')

    # Create the QR code
    qr = qrcode.QRCode(version=1, error_correction=qrcode.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='blue', back_color='white')

    # Save QR image to a BytesIO object
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    # Encode the image to base64 for embedding in HTML
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

    # Generate the download link
    img_io.seek(0)
    img_data = base64.b64encode(img_io.getvalue()).decode('utf-8')

    # Return the template with the QR code and image data
    return render_template('index.html', qr_code=img_base64, img_data=img_data)

@app.route('/download')
def download_qr():
    # Get the image data from request
    img_data = request.args.get('img_data')

    # Convert from base64 to binary data and send the file
    img_binary = base64.b64decode(img_data)
    return send_file(io.BytesIO(img_binary), mimetype='image/png', as_attachment=True, download_name='qr_code.png')

