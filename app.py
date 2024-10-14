from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()  # Cargar las variables de entorno desde el archivo .env

# if not app.debug:
#     handler = RotatingFileHandler('/home/jaimepar/backend/error.log', maxBytes=10000, backupCount=1)
#     handler.setLevel(logging.ERROR)
#     app.logger.addHandler(handler)

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'mail.jaimepardo.cl'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')

mail = Mail(app)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/protactiv', methods=['POST', 'OPTIONS'])
def send_email():
    if request.method == 'OPTIONS':
        # Responder a la solicitud de preflight
        return _build_cors_preflight_response()

    data = request.get_json()  # Recibe los datos enviados en formato JSON desde el frontend
    nombre = data.get('nombre')
    email = data.get('email')
    telefono = data.get('telefono')
    asunto = data.get('asunto')
    mensaje = data.get('mensaje')

    # Crear el mensaje de correo
    msg = Message(subject=asunto,
                  sender= app.config['MAIL_USERNAME'],  # Tu email
                  recipients=['contacto@jaimepardo.cl'])  # Email al que deseas enviar el mensaje

    # Formatear el cuerpo del mensaje con los datos recibidos
    msg.body = f"Nombre: {nombre}\nTeléfono: {telefono}\nEmail: {email}\nMensaje:\n{mensaje}"

    try:
        # Enviar el correo
        mail.send(msg)
        return jsonify({'message': 'Correo enviado con éxito'}), 200
    except Exception as e:
        return jsonify({'message': 'Error al enviar el correo', 'error': str(e)}), 500

# Funciones auxiliares para manejar CORS de preflight
def _build_cors_preflight_response():
    response = jsonify({'message': 'CORS preflight successful'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/index')
def index():
    return "Servidor Flask funcionando"

if __name__ == '__main__':
    app.run(debug=True)