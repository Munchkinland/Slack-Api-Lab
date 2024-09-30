import os
import logging
from slack_sdk import WebClient
from datetime import datetime, timedelta
from random import choice
from models import Task, Timer
from modules.trello_integration import (
    create_card,
    create_new_list_on_trello,
    set_card_due_date,
    add_comment_to_card,
    move_card_to_list,
    assign_card_member,
    get_card_comments,
    set_card_priority
)


def create_task(user_id, task_name, db):
    if not task_name:
        return "Por favor, proporciona un nombre para la tarea. Uso: /create_task [nombre de la tarea]"

    logging.info(f"Intentando crear tarea: {task_name}")
    # Crear la tarea en Trello
    trello_created = create_card(task_name)
    if trello_created:
        # Guardar la tarea en la base de datos
        task = Task(name=task_name, user_id=user_id, trello_card_id=trello_created['id'])
        db.session.add(task)
        db.session.commit()
        message = f"Tarea '{task_name}' creada en Trello y guardada en la base de datos."
        logging.info(message)
    else:
        message = "Hubo un error al crear la tarea en Trello. Verifica los logs para más detalles."
        logging.error(message)

    return message

def create_new_list(user_id, list_name):
    logging.info(f"Attempting to create new list: {list_name}")
    if create_new_list_on_trello(list_name):
        message = f"Nueva lista '{list_name}' creada con éxito en Trello."
        logging.info(message)
    else:
        message = f"Fallo al crear la lista '{list_name}' en Trello."
        logging.error(message)
    return message

def set_due_date(user_id, task_id, due_date, db):
    if not task_id.isdigit():
        return "Por favor, proporciona un ID de tarea válido. Uso: /set_due_date [task_id] [YYYY-MM-DD]"
    
    task = db.session.query(Task).filter_by(id=int(task_id), user_id=user_id).first()
    if not task:
        return f"No se encontró ninguna tarea con ID {task_id}."
    
    try:
        due_date = datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        return "Formato de fecha inválido. Usa YYYY-MM-DD."
    
    if set_card_due_date(task.trello_card_id, due_date):
        task.due_date = due_date
        db.session.commit()
        return f"Fecha límite para la tarea '{task.name}' establecida para {due_date.strftime('%Y-%m-%d')}."
    else:
        return "Error al establecer la fecha límite en Trello."

def upcoming_tasks(user_id, db):
    today = datetime.now().date()
    week_later = today + timedelta(days=7)
    tasks = db.session.query(Task).filter(
        Task.user_id == user_id,
        Task.due_date.between(today, week_later)
    ).order_by(Task.due_date).all()
    
    if not tasks:
        return "No tienes tareas pendientes para la próxima semana."
    
    task_list = "\n".join([f"- {task.name} (Fecha límite: {task.due_date.strftime('%Y-%m-%d')})" for task in tasks])
    return f"Tus tareas próximas:\n{task_list}"

def add_comment(user_id, task_id, comment, db):
    if not task_id.isdigit():
        return "Por favor, proporciona un ID de tarea válido. Uso: /add_comment [task_id] [comentario]"
    
    task = db.session.query(Task).filter_by(id=int(task_id), user_id=user_id).first()
    if not task:
        return f"No se encontró ninguna tarea con ID {task_id}."
    
    if add_comment_to_card(task.trello_card_id, comment):
        return f"Comentario agregado a la tarea '{task.name}': {comment}"
    else:
        return "Error al agregar el comentario en Trello."

def view_comments(user_id, task_id, db):
    if not task_id.isdigit():
        return "Por favor, proporciona un ID de tarea válido. Uso: /view_comments [task_id]"
    
    task = db.session.query(Task).filter_by(id=int(task_id), user_id=user_id).first()
    if not task:
        return f"No se encontró ninguna tarea con ID {task_id}."
    
    comments = get_card_comments(task.trello_card_id)
    if comments:
        comment_list = "\n".join([f"- {comment}" for comment in comments])
        return f"Comentarios para la tarea '{task.name}':\n{comment_list}"
    else:
        return f"No se encontraron comentarios para la tarea '{task.name}' o error al obtener los comentarios."

def assign_task(user_id, task_id, assigned_user, db):
    if not task_id.isdigit():
        return "Por favor, proporciona un ID de tarea válido. Uso: /assign_task [task_id] [@usuario]"
    
    task = db.session.query(Task).filter_by(id=int(task_id), user_id=user_id).first()
    if not task:
        return f"No se encontró ninguna tarea con ID {task_id}."
    
    if not assigned_user.startswith('@'):
        return "Por favor, proporciona un usuario válido en formato @usuario."
    
    if assign_card_member(task.trello_card_id, assigned_user):
        task.assigned_to = assigned_user
        db.session.commit()
        return f"Tarea '{task.name}' asignada a {assigned_user}."
    else:
        return f"Error al asignar la tarea a {assigned_user} en Trello."

def my_tasks(user_id, db):
    tasks = db.session.query(Task).filter_by(assigned_to=user_id).all()
    if not tasks:
        return "No tienes tareas asignadas."
    
    task_list = "\n".join([f"- {task.name} (ID: {task.id})" for task in tasks])
    return f"Tareas asignadas a ti:\n{task_list}"

def set_priority(user_id, task_id, priority, db):
    if not task_id.isdigit():
        return "Por favor, proporciona un ID de tarea válido. Uso: /set_priority [task_id] [high/medium/low]"
    
    task = db.session.query(Task).filter_by(id=int(task_id), user_id=user_id).first()
    if not task:
        return f"No se encontró ninguna tarea con ID {task_id}."
    
    valid_priorities = ['high', 'medium', 'low']
    if priority.lower() not in valid_priorities:
        return "Prioridad inválida. Usa 'high', 'medium', o 'low'."
    
    if set_card_priority(task.trello_card_id, priority.lower()):
        task.priority = priority.lower()
        db.session.commit()
        return f"Prioridad de la tarea '{task.name}' establecida a {priority}."
    else:
        return "Error al establecer la prioridad de la tarea en Trello."

def priority_list(user_id, db):
    tasks = db.session.query(Task).filter_by(user_id=user_id).order_by(
        db.case(
            {'high': 1, 'medium': 2, 'low': 3},
            value=Task.priority
        )
    ).all()
    
    if not tasks:
        return "No tienes tareas."
    
    task_list = "\n".join([f"- [{task.priority.upper()}] {task.name} (ID: {task.id})" for task in tasks])
    return f"Tus tareas por prioridad:\n{task_list}"

def start_timer(user_id, task_name, db):
    task = None
    if task_name:
        task = db.session.query(Task).filter_by(name=task_name, user_id=user_id).first()
        if not task:
            return f"No se encontró la tarea '{task_name}'."

    timer = Timer(user_id=user_id, task_id=task.id if task else None)
    db.session.add(timer)
    db.session.commit()

    if task:
        return f"Temporizador iniciado para la tarea '{task_name}'."
    else:
        return "Temporizador iniciado."

def stop_timer(user_id, db):
    timer = db.session.query(Timer).filter_by(user_id=user_id, end_time=None).first()
    if timer:
        timer.end_time = datetime.utcnow()
        db.session.commit()

        elapsed = (timer.end_time - timer.start_time).total_seconds()
        hours, remainder = divmod(int(elapsed), 3600)
        minutes, seconds = divmod(remainder, 60)
        message = f"Temporizador detenido. Tiempo transcurrido: {hours}h {minutes}m {seconds}s."
    else:
        message = "No hay un temporizador en marcha."

    return message

def get_tip():
    tips = [
        "Divide tareas grandes en tareas más pequeñas.",
        "Prioriza tus tareas con una lista.",
        "Toma descansos cortos regularmente.",
        "Elimina distracciones mientras trabajas.",
        "Establece objetivos claros para el día.",
        "Usa la técnica Pomodoro para mejorar tu concentración.",
        "Organiza tu espacio de trabajo para aumentar la productividad.",
        "Revisa y actualiza tus tareas diariamente."
    ]
    tip = choice(tips)
    message = f"Consejo de productividad: {tip}"
    return message

def break_reminder(user_id, slack_client, scheduler):
    message = "¡Es hora de tomar un descanso! Estírate y relaja la mente."
    slack_client.chat_postMessage(channel=user_id, text=message)
    scheduler.add_job(lambda: break_reminder(user_id, slack_client, scheduler), 'interval', hours=1)

def cancel_break_reminder(user_id, slack_client, scheduler):
    scheduler.remove_all_jobs()
    message = "Recordatorios de descanso cancelados."
    slack_client.chat_postMessage(channel=user_id, text=message)

def start_pomodoro(user_id, db, scheduler):
  # Iniciar una sesión de Pomodoro
  timer = Timer(user_id=user_id)
  db.session.add(timer)
  db.session.commit()

  # Programar el recordatorio al finalizar Pomodoro (25 minutos)
  run_time = datetime.utcnow() + timedelta(minutes=25)
  scheduler.add_job(send_pomodoro_end, 'date', run_date=run_time, args=[user_id, db])

  message = "Sesión Pomodoro iniciada. Trabaja durante 25 minutos."
  return message

def send_pomodoro_end(user_id, db):
  slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
  slack_client = WebClient(token=slack_bot_token)
  message = "¡Tu sesión Pomodoro ha terminado! Toma un descanso de 5 minutos."
  slack_client.chat_postMessage(channel=user_id, text=message)

def list_tasks(user_id, db):
  tasks = db.session.query(Task).filter_by(user_id=user_id).all()
  if not tasks:
      return "No tienes tareas creadas."
  task_list = "\n".join([f"- {task.name} (ID: {task.id})" for task in tasks])
  message = f"Tus tareas:\n{task_list}"
  return message

def delete_task(user_id, task_id_str, db):
  if not task_id_str.isdigit():
      return "Por favor, proporciona un ID válido de tarea. Uso: /delete_task [ID]"

  task_id = int(task_id_str)
  task = db.session.query(Task).filter_by(id=task_id, user_id=user_id).first()
  if task:
      db.session.delete(task)
      db.session.commit()
      message = f"Tarea '{task.name}' eliminada."
  else:
      message = f"No se encontró la tarea con ID '{task_id}'."
  return message

def stats(user_id, db):
  # Calcular tiempo total trabajado
  timers = db.session.query(Timer).filter_by(user_id=user_id).all()
  total_seconds = sum([(timer.end_time - timer.start_time).total_seconds() for timer in timers if timer.end_time])
  hours, remainder = divmod(int(total_seconds), 3600)
  minutes, seconds = divmod(remainder, 60)

  # Contar Pomodoros
  pomodoros = db.session.query(Timer).count()

  message = f"**Estadísticas de Productividad**\nTiempo total trabajado: {hours}h {minutes}m {seconds}s.\nSesiones Pomodoro completadas: {pomodoros}."
  return message

def recent_tasks(user_id, db):
  tareas = db.session.query(Task).filter_by(user_id=user_id).order_by(Task.created_at.desc()).limit(5).all()
  if not tareas:
      return "No tienes tareas recientes."
  task_list = "\n".join([f"- {task.name} (Creada el: {task.created_at.strftime('%Y-%m-%d')})" for task in tareas])
  message = f"Tus tareas recientes:\n{task_list}"
  return message

def timer_status(user_id, db):
  timer = db.session.query(Timer).filter_by(user_id=user_id, end_time=None).first()
  if timer:
      start_time = timer.start_time
      elapsed = datetime.utcnow() - start_time
      minutes, seconds = divmod(elapsed.seconds, 60)
      hours, minutes = divmod(minutes, 60)
      message = f"Tienes un temporizador activo desde {start_time.strftime('%H:%M:%S')} UTC. Tiempo transcurrido: {hours}h {minutes}m {seconds}s."
  else:
      message = "No tienes temporizadores activos."
  return message