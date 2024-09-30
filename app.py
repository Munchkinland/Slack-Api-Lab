from flask import Flask, request, make_response
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
from dotenv import load_dotenv
import logging
import os
from modules import slack_commands, trello_integration
from models import db
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler

# Cargar variables de entorno
load_dotenv()

# Configurar el logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Inicializar Flask-Migrate
migrate = Migrate(app, db)

# Configuración de Slack
slack_signing_secret = os.getenv("SLACK_SIGNING_SECRET")
slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
signature_verifier = SignatureVerifier(signing_secret=slack_signing_secret)
slack_client = WebClient(token=slack_bot_token)

# Inicializar el scheduler
scheduler = BackgroundScheduler()
scheduler.start()

@app.route('/', methods=['GET'])
def index():
    return "La aplicación Flask está funcionando correctamente."

@app.route('/slash/events', methods=['POST'])
def slash_events():
    if not signature_verifier.is_valid_request(request.get_data(), request.headers):
        logging.warning("Firma de solicitud inválida. Rechazando la solicitud.")
        return make_response("Invalid request signature.", 403)

    logging.info("Solicitud recibida en /slash/events")
    try:
        data = request.form
        command = data.get('command')
        user_id = data.get('user_id')
        text = data.get('text')
        response_url = data.get('response_url')

        logging.info(f"Datos recibidos: command={command}, user_id={user_id}, text={text}")

        # Manejar los comandos
        command_handlers = {
            '/view_comments': lambda: trello_integration.view_comments(text),  # task_id en text
            '/assign_task': lambda: process_assign_task(text),  # task_id y @usuario en text
            '/my_tasks': lambda: trello_integration.my_tasks(user_id),
            '/set_priority': lambda: process_set_priority(text),  # task_id y prioridad en text
            '/priority_list': lambda: trello_integration.priority_list(user_id),
            '/create_task': lambda: slack_commands.create_task(user_id, text, db),
            '/start_timer': lambda: slack_commands.start_timer(user_id, text, db),
            '/stop_timer': lambda: slack_commands.stop_timer(user_id, db),
            '/get_tip': lambda: slack_commands.get_tip(),
            '/break_reminder': lambda: slack_commands.break_reminder(user_id, slack_client, scheduler),
            '/cancel_break_reminder': lambda: slack_commands.cancel_break_reminder(user_id, scheduler),
            '/start_pomodoro': lambda: slack_commands.start_pomodoro(user_id, db, scheduler),
            '/list_tasks': lambda: slack_commands.list_tasks(user_id, db),
            '/delete_task': lambda: process_delete_task(text, user_id),  # task_id en text
            '/stats': lambda: slack_commands.stats(user_id, db),
            '/recent_tasks': lambda: slack_commands.recent_tasks(user_id, db),
            '/timer_status': lambda: slack_commands.timer_status(user_id, db),
        }

        handler = command_handlers.get(command)
        if handler:
            response = handler()
            logging.info(f"Respuesta enviada: {response}")
            return response
        else:
            logging.warning("Comando no reconocido.")
            return make_response("Comando no reconocido.", 200)
    except Exception as e:
        logging.error(f"Error al manejar el comando: {e}")
        return make_response("Error interno del servidor.", 500)

def process_assign_task(text):
    """ Procesar /assign_task para manejar múltiples parámetros. """
    parts = text.split()
    if len(parts) != 2:
        return "Por favor, proporciona un ID de tarea válido y un usuario. Uso: /assign_task [task_id] [@usuario]"
    task_id, assigned_user = parts
    return trello_integration.assign_task(task_id, assigned_user)

def process_set_priority(text):
    """ Procesar /set_priority para manejar múltiples parámetros. """
    parts = text.split()
    if len(parts) != 2:
        return "Por favor, proporciona un ID de tarea válido y una prioridad. Uso: /set_priority [task_id] [high/medium/low]"
    task_id, priority = parts
    return trello_integration.set_priority(task_id, priority)

def process_delete_task(text, user_id):
    """ Procesar /delete_task para manejar el ID de tarea. """
    if not text.isdigit():
        return "Por favor, proporciona un ID de tarea válido. Uso: /delete_task [ID]"
    return slack_commands.delete_task(user_id, text, db)

if __name__ == "__main__":
    app.run(port=5000)
