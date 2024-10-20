import eventlet
eventlet.monkey_patch()

from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io
import base64
import cv2
import pytesseract
import re
from flask_cors import CORS
import ssl

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize Flask and Flask-SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app, resources={r"/*": {"origins": "*"}})

# Load the pre-trained CNN model for image classification
model = load_model('imageclassifier.h5')

# Preprocess image for OCR
def preprocess_image(image_bytes):
    np_img = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh

# Function to extract specific details from the OCR output
def extract_details(text):
    # Initialize details dictionary
    details = {
        "mrp": None,
        "pack_size": None,
        "mfg_date": None,
        "exp_date": None,
        "brand_name": None,
        "lot_no": None
    }

    # Split the text into lines
    lines = text.split('\n')

    # Iterate over lines to find and assign values based on their labels
    for line in lines:
        line = line.strip()  # Clean up whitespace

        # Assign values based on their label
        if "mrp" in line.lower():
            details['mrp'] = line.split(':', 1)[1].strip() if ':' in line else None
        elif "pack size" in line.lower():
            details['pack_size'] = line.split(':', 1)[1].strip() if ':' in line else None
        elif "mfg date" in line.lower():
            details['mfg_date'] = line.split(':', 1)[1].strip() if ':' in line else None
        elif "exp date" in line.lower():
            details['exp_date'] = line.split(':', 1)[1].strip() if ':' in line else None
        elif "brand name" in line.lower():
            details['brand_name'] = line.split(':', 1)[1].strip() if ':' in line else None
        elif "lot no" in line.lower():
            details['lot_no'] = line.split(':', 1)[1].strip() if ':' in line else None

    return details



# Function to clean and format OCR output
def format_ocr_output(text):
    # Remove excessive whitespace and split lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Join lines with proper formatting
    formatted_text = "\n".join(lines)

    # Extract details
    details = extract_details(formatted_text)

    return formatted_text, details

# Root route to serve index.html and other static files
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static_file(path):
    return send_from_directory('.', path)

# WebSocket route for classification and OCR
@socketio.on('message')
def handle_message(data):
    try:
        task = data.get('task')
        base64_image = data.get('image')
        image_bytes = base64.b64decode(base64_image)
        img = Image.open(io.BytesIO(image_bytes))

        if task == 'classify':
            # Preprocess for classification (CNN)
            img = img.resize((254, 254))
            img = np.array(img) / 255.0
            img = np.expand_dims(img, axis=0)
            prediction = model.predict(img)
            result = 'rotten' if prediction[0][0] > 0.5 else 'fresh'
            emit('message', {'classification': result})

        elif task == 'ocr':
            # Preprocess and extract text for OCR
            processed_img = preprocess_image(image_bytes)
            raw_text = pytesseract.image_to_string(processed_img)

            # Format the extracted text and get details
            formatted_text, details = format_ocr_output(raw_text)

            # Send structured response
            emit('message', {
                'text': formatted_text,  # Nicely formatted OCR output
                'details': details  # Structured details extracted
            })

    except Exception as e:
        emit('error', {'error': str(e)})

if __name__ == '__main__':
    # Setup SSL context for HTTPS
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

    # Start the server with eventlet and SSL
    eventlet.wsgi.server(
        eventlet.wrap_ssl(eventlet.listen(('0.0.0.0', 5000)),
                          certfile='cert.pem',
                          keyfile='key.pem',
                          server_side=True),
        app
    )
