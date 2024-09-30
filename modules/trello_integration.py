import os
import requests
import logging

def create_card(name):
    api_key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_TOKEN")
    board_id = os.getenv("TRELLO_BOARD_ID")

    logging.info(f"Intentando crear tarjeta: {name}")
    url = f"https://api.trello.com/1/boards/{board_id}/lists?key={api_key}&token={token}"
    response = requests.get(url)
    if response.ok:
        lists = response.json()
        if lists:
            list_id = lists[0]['id']  # Tomar la primera lista
            logging.info(f"ID de la lista obtenido: {list_id}")
            card_url = "https://api.trello.com/1/cards"
            query = {'key': api_key, 'token': token, 'idList': list_id, 'name': name}
            card_response = requests.post(card_url, params=query)
            if card_response.ok:
                logging.info("Tarjeta creada exitosamente")
                return card_response.json()  # Retorna la tarjeta creada en formato JSON
            else:
                logging.error(f"Error al crear la tarjeta: {card_response.status_code} - {card_response.text}")
                return None
        else:
            logging.error("No se encontraron listas en el tablero")
    else:
        logging.error(f"Error al obtener listas del tablero: {response.status_code} - {response.text}")
    return None

def create_new_list_on_trello(list_name):
    api_key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_TOKEN")
    board_id = os.getenv("TRELLO_BOARD_ID")

    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    params = {
        'key': api_key,
        'token': token,
        'name': list_name
    }
    response = requests.post(url, params=params)
    
    if response.ok:
        logging.info(f"Lista '{list_name}' creada en Trello.")
        return response.json()
    else:
        logging.error(f"Error al crear la lista en Trello: {response.text}")
        return None

def set_card_due_date(card_id, due_date):
    api_key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_TOKEN")

    url = f"https://api.trello.com/1/cards/{card_id}"
    params = {
        'key': api_key,
        'token': token,
        'due': due_date.isoformat()
    }
    response = requests.put(url, params=params)
    
    if response.ok:
        logging.info(f"Fecha límite '{due_date}' establecida para la tarjeta {card_id}")
        return True
    else:
        logging.error(f"Error al establecer fecha límite en Trello: {response.text}")
        return False

def add_comment_to_card(card_id, comment):
    api_key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_TOKEN")

    url = f"https://api.trello.com/1/cards/{card_id}/actions/comments"
    params = {
        'key': api_key,
        'token': token,
        'text': comment
    }
    response = requests.post(url, params=params)
    
    if response.ok:
        logging.info(f"Comentario agregado a la tarjeta {card_id}: {comment}")
        return True
    else:
        logging.error(f"Error al agregar comentario en Trello: {response.text}")
        return False

def get_card_comments(card_id):
    api_key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_TOKEN")

    url = f"https://api.trello.com/1/cards/{card_id}/actions?filter=commentCard"
    params = {
        'key': api_key,
        'token': token
    }
    response = requests.get(url, params=params)
    
    if response.ok:
        comments = [action['data']['text'] for action in response.json()]
        logging.info(f"Comentarios obtenidos de la tarjeta {card_id}")
        return comments
    else:
        logging.error(f"Error al obtener comentarios en Trello: {response.text}")
        return []

def assign_card_member(card_id, member_id):
    api_key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_TOKEN")

    url = f"https://api.trello.com/1/cards/{card_id}/idMembers"
    params = {
        'key': api_key,
        'token': token,
        'value': member_id
    }
    response = requests.post(url, params=params)
    
    if response.ok:
        logging.info(f"Miembro {member_id} asignado a la tarjeta {card_id}")
        return True
    else:
        logging.error(f"Error al asignar miembro en Trello: {response.text}")
        return False

def set_card_priority(card_id, priority):
    api_key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_TOKEN")

    # Suponemos que la prioridad se establece como una etiqueta en Trello
    priority_labels = {
        'high': 'label_id_high',
        'medium': 'label_id_medium',
        'low': 'label_id_low'
    }
    
    label_id = priority_labels.get(priority.lower())
    if not label_id:
        logging.error(f"Prioridad {priority} no reconocida.")
        return False

    url = f"https://api.trello.com/1/cards/{card_id}/idLabels"
    params = {
        'key': api_key,
        'token': token,
        'value': label_id
    }
    response = requests.post(url, params=params)
    
    if response.ok:
        logging.info(f"Prioridad '{priority}' asignada a la tarjeta {card_id}")
        return True
    else:
        logging.error(f"Error al establecer prioridad en Trello: {response.text}")
        return False

def create_new_list_on_trello(list_name):
    api_key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_TOKEN")
    board_id = os.getenv("TRELLO_BOARD_ID")

    logging.info(f"Intentando crear una nueva lista: {list_name}")
    logging.info(f"API Key: {api_key[:5]}... Token: {token[:5]}... Board ID: {board_id}")

    # Crear una nueva lista en el tablero
    url = "https://api.trello.com/1/lists"
    query = {
        'key': api_key,
        'token': token,
        'name': list_name,
        'idBoard': board_id
    }
    response = requests.post(url, params=query)

    if response.ok:
        logging.info("Lista creada exitosamente")
        return response.json()  # Devuelve la información de la lista creada
    else:
        logging.error(f"Error al crear la lista: {response.status_code} - {response.text}")
        return None
    
def set_card_due_date(card_id, due_date):
    api_key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_TOKEN")

    logging.info(f"Intentando establecer la fecha de vencimiento para la tarjeta ID: {card_id} a {due_date}")
    
    url = f"https://api.trello.com/1/cards/{card_id}"
    query = {
        'key': api_key,
        'token': token,
        'due': due_date  # Fecha en formato ISO 8601
    }
    response = requests.put(url, params=query)

    if response.ok:
        logging.info("Fecha de vencimiento establecida exitosamente")
        return True
    else:
        logging.error(f"Error al establecer la fecha de vencimiento: {response.status_code} - {response.text}")
        return False
def add_comment_to_card(card_id, comment):
    api_key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_TOKEN")

    logging.info(f"Intentando añadir un comentario a la tarjeta ID: {card_id}")
    
    url = f"https://api.trello.com/1/cards/{card_id}/actions/comments"
    query = {
        'key': api_key,
        'token': token,
        'text': comment
    }
    response = requests.post(url, params=query)

    if response.ok:
        logging.info("Comentario añadido exitosamente")
        return True
    else:
        logging.error(f"Error al añadir comentario: {response.status_code} - {response.text}")
        return False
def move_card_to_list(card_id, list_id):
    api_key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_TOKEN")

    logging.info(f"Intentando mover la tarjeta ID: {card_id} a la lista ID: {list_id}")
    
    url = f"https://api.trello.com/1/cards/{card_id}"
    query = {
        'key': api_key,
        'token': token,
        'idList': list_id
    }
    response = requests.put(url, params=query)

    if response.ok:
        logging.info("Tarjeta movida exitosamente")
        return True
    else:
        logging.error(f"Error al mover la tarjeta: {response.status_code} - {response.text}")
        return False
def assign_card_member(card_id, member_id):
    api_key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_TOKEN")

    logging.info(f"Intentando asignar el miembro ID: {member_id} a la tarjeta ID: {card_id}")

    url = f"https://api.trello.com/1/cards/{card_id}/idMembers"
    query = {
        'key': api_key,
        'token': token,
        'value': member_id
    }
    response = requests.post(url, params=query)

    if response.ok:
        logging.info("Miembro asignado exitosamente a la tarjeta")
        return True
    else:
        logging.error(f"Error al asignar el miembro: {response.status_code} - {response.text}")
        return False
def set_card_priority(card_id, priority_label):
    api_key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_TOKEN")

    logging.info(f"Intentando establecer la prioridad para la tarjeta ID: {card_id} a {priority_label}")

    # Suponiendo que ya tienes las etiquetas de prioridad predefinidas en Trello
    label_ids = {
        "alta": "label_id_for_high_priority",
        "media": "label_id_for_medium_priority",
        "baja": "label_id_for_low_priority"
    }

    label_id = label_ids.get(priority_label.lower())
    if not label_id:
        logging.error("Prioridad no válida, debe ser 'alta', 'media' o 'baja'")
        return False

    url = f"https://api.trello.com/1/cards/{card_id}/idLabels"
    query = {
        'key': api_key,
        'token': token,
        'value': label_id
    }
    response = requests.post(url, params=query)

    if response.ok:
        logging.info(f"Prioridad establecida exitosamente para la tarjeta ID: {card_id}")
        return True
    else:
        logging.error(f"Error al establecer la prioridad: {response.status_code} - {response.text}")
        return False

def get_card_comments(card_id):
    api_key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_TOKEN")

    logging.info(f"Intentando obtener comentarios de la tarjeta ID: {card_id}")

    url = f"https://api.trello.com/1/cards/{card_id}/actions?filter=commentCard"
    query = {
        'key': api_key,
        'token': token
    }
    response = requests.get(url, params=query)

    if response.ok:
        comments = response.json()
        logging.info(f"Comentarios obtenidos: {comments}")
        return comments
    else:
        logging.error(f"Error al obtener comentarios: {response.status_code} - {response.text}")
        return []