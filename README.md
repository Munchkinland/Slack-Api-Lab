# Slack-Api-Lab

🚀 Integración de Slack con Backend🚀

Este proyecto demuestra cómo integrar una aplicación de productividad con Slack, utilizando comandos slash personalizados para interactuar con Trello y gestionar tareas en tiempo real. También se muestra cómo utilizar ngrok para exponer un servidor local a una URL pública, facilitando el desarrollo y la prueba de la integración.
Características principales

    Comandos slash en Slack para gestionar tareas.
    Integración con Trello para crear y gestionar tarjetas y listas directamente desde Slack.
    Temporizadores y estadísticas de productividad para un mejor seguimiento del tiempo.
    Desarrollo local con ngrok, permitiendo el forwarding de tu servidor Flask a Slack.

Comandos disponibles

    /create_task [nombre de la tarea]
    Crea una nueva tarea en Trello y la guarda en la base de datos.

    /start_timer [nombre de la tarea]
    Inicia un temporizador asociado a una tarea específica.

    /stop_timer
    Detiene el temporizador y muestra el tiempo transcurrido.

    /assign_task [task_id] [@usuario]
    Asigna una tarea a un usuario de Slack.

    /set_priority [task_id] [high/medium/low]
    Establece la prioridad de una tarea en Trello.

    /list_tasks
    Muestra todas las tareas creadas por el usuario.

    /my_tasks
    Muestra todas las tareas asignadas al usuario en Trello.

    /delete_task [task_id]
    Elimina una tarea en Trello y de la base de datos.

    /get_tip
    Proporciona un consejo de productividad.

    /start_pomodoro
    Inicia una sesión de trabajo Pomodoro de 25 minutos.

    /break_reminder
    Envía un recordatorio para tomar un descanso cada hora.

    /cancel_break_reminder
    Cancela los recordatorios de descanso.

    /stats
    Muestra estadísticas de productividad, como tiempo total trabajado y número de sesiones Pomodoro completadas.

Requisitos

    Python 3.x
    Flask
    Slack SDK
    Trello API
    ngrok
    SQLAlchemy (para la base de datos)
    APScheduler (para la gestión de temporizadores)

Instalación

    Clonar el repositorio:

    git clone https://github.com/Munchkinland/Slack-Api-Lab

Instalar dependencias:

    pip install -r requirements.txt

Configurar variables de entorno:

    SLACK_SIGNING_SECRET=<tu-slack-signing-secret>
    SLACK_BOT_TOKEN=<tu-slack-bot-token>
    TRELLO_API_KEY=<tu-trello-api-key>
    TRELLO_TOKEN=<tu-trello-token>
    TRELLO_BOARD_ID=<tu-trello-board-id>
    DATABASE_URL=<url-de-tu-base-de-datos>

Iniciar migracion base de datos:

    python manage.py

Iniciar el servidor Flask

    python app.py

Configurar ngrok:

Si estás desarrollando localmente, utiliza ngrok para exponer tu servidor

    ngrok http 5000

    Copia la URL que te proporciona ngrok y configúrala como el Request URL en tu app de Slack, bajo Interactivity & Shortcuts y Slash Commands.

    Configurar Slack:
        Ve a tu Panel de aplicaciones de Slack.
        Crea una nueva aplicación.
        En Slash Commands, agrega los comandos mencionados arriba y apunta a la URL de ngrok.
        En OAuth & Permissions, asegúrate de agregar los scopes necesarios, como commands, chat:write, y cualquier otro que necesites para interactuar con Slack y Trello.

Uso

    En Slack, ejecuta los comandos slash como /create_task, /start_timer, etc., y observa cómo interactúan con Trello y el backend.

Estructura del proyecto

  <img width="449" alt="image" src="https://github.com/user-attachments/assets/156b7929-1daa-4018-ba6e-1c0b39b22c65">

Contribuir

    Haz un fork del proyecto.
    Crea tu feature branch (git checkout -b feature/nueva-funcionalidad).
    Haz commit de tus cambios (git commit -m 'Agregar nueva funcionalidad').
    Push a la rama (git push origin feature/nueva-funcionalidad).
    Abre un Pull Request.

Licencia

    Este proyecto está bajo la Licencia MIT





    

    


  



