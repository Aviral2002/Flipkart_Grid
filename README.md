# Flipkart Grid 2024

This project provides a web application for detecting the freshness of fruits and vegetables, extracting product details using OCR, and recognizing brands with counting. It leverages a Convolutional Neural Network (CNN) for image classification, Tesseract OCR for text extraction, and Roboflow for brand recognition. Communication between the front-end and back-end is facilitated by WebSockets.

Video Demo :: https://youtu.be/rdapySG5OB0?si=FxbVSFYDMD1X_BMB

## Main Features

* **Freshness Detection:** Classifies images of fruits and vegetables as either "fresh" or "rotten" using a pre-trained CNN model.
* **OCR (Optical Character Recognition):** Extracts product details like MRP, pack size, manufacturing date, expiry date, brand name, and lot number from images.
* **Brand Recognition and Counting:** Detects and counts the occurrences of specific brands in an image using a Roboflow model.
* **WebSockets:** Enables real-time communication between the client and the server for seamless image submission and result retrieval.
* **Drag-and-drop/Upload:** Allows users to either drag and drop an image or upload it through a file input.
* **Camera Capture:**  Captures images directly from the user's camera (with front and back camera switching).

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/freshness-detection.git
   cd freshness-detection
content_copy
Use code with caution.
Markdown

Create a Virtual Environment (Recommended):
```
python -m venv env
env\Scripts\activate  (Windows)
source env/bin/activate (macOS/Linux)

```
Use code with caution.

Install Dependencies:
```
pip install -r requirements.txt
```

Install Tesseract OCR:

Download the Tesseract OCR installer for your operating system from https://github.com/UB-Mannheim/tesseract/wiki and install it.

Important: Make sure to add the Tesseract OCR installation directory to your system's PATH environment variable (e.g., C:\Program Files\Tesseract-OCR). Update the path in app.py if it's different.

Obtain SSL Certificates (cert.pem, key.pem):
For local development, you can generate self-signed certificates. For production, you'll need certificates from a trusted Certificate Authority. See the section on HTTPS below for more.

Download the trained model:

Download the 'imageclassifier.h5' model file and place it in the project's root directory.

Usage Examples

Running the Application:
```
python app.py
```


This will start the Flask development server. Open your web browser and navigate to https://127.0.0.1:5000 (or the URL shown in your terminal). Note that the web app uses https, which is addressed in the next section.

HTTPS (Local Development):
To run the app locally with HTTPS, you need to generate self-signed certificates. One way to do this is using OpenSSL:
```
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

```


When prompted for information about your certificate, you can enter dummy values as this is for local development only. Make sure these cert.pem and key.pem files are in the same directory as app.py.
Modify the filenames in app.py if necessary.

Now, the python command will work. Note: Your browser may warn you that the certificate is not trusted. You can safely bypass this for local testing.

Using the Application:

Drag and Drop/Upload: Drag an image onto the designated area or click to select an image from your local file system.

Camera Capture: Click the "Capture" button to take a picture using your camera. The "Switch Camera" button toggles between front and back cameras. Use the "Turn Camera Off" button when you don't need camera access anymore.

Task Selection: Choose the task you wish to perform (classify, OCR, or brand recognition) using the dropdown menu.

Results: The results of the chosen task will be displayed in the result area in JSON format.

Project Structure

.gitignore: Specifies files and directories to be ignored by Git.

app.py: Contains the Flask back-end code for image processing and WebSocket communication.

FreshnessIndex.keras: The saved Keras model for freshness detection.

Getting Started.ipynb: A Jupyter Notebook to guide through setting up the environment and training the model (not needed for just running).

index.html: Contains the HTML, CSS, and JavaScript for the front-end interface.

README.md: This file.

requirements.txt: Lists all the required Python packages.

content_copy
Use code with caution.

requirements.txt

```

tensorflow==2.17.0
Flask==2.3.3
Flask-Cors==3.0.10
requests==2.32.3
Flask-SocketIO==5.3.0
opencv-python==4.10.0.84
Pillow==10.1.0
pytesseract==0.3.12
eventlet==0.33.3
python-dotenv==1.0.0

```

Key changes and explanations:

* **Clearer Feature Descriptions:**  Expanded the descriptions of the core functionalities.
* **Detailed Setup:** More specific step-by-step instructions, including virtual environment setup and Tesseract installation, and obtaining SSL certificates.
* **HTTPS Instructions:** Added a section explaining how to generate self-signed certificates for local development with HTTPS, which is required by the provided `app.py`.
* **Model Download:** Added a step for downloading the `imageclassifier.h5` model file, as it's not in the repo but referenced in `app.py`.
* **Updated `requirements.txt`:**  Includes `pytesseract`, `eventlet`, `Pillow` and other missing dependencies based on the contents of `app.py` and other files.  Also pinned versions to ensure compatibility.
* **Clarified Frontend to Backend Communication:** Emphasized the role of WebSockets and clarified how the frontend interacts with both the Flask backend and Roboflow directly. The example usage now explains the web app elements.





