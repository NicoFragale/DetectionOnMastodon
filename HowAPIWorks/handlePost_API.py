import requests
import logging
import time
from datetime import datetime, timedelta

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_http_error(response):
    status_code = response.status_code
    match status_code:
        case 400:
            logging.error("Bad Request: The server could not understand the request.")
        case 401:
            logging.error("Unauthorized: Authentication is required and has failed or has not been provided.")
        case 403:
            logging.error("Forbidden: The server understood the request, but refuses to authorize it.")
        case 404:
            logging.error("Not Found: The requested resource could not be found.")
        case 500:
            logging.error("Internal Server Error: The server encountered an internal error and was unable to complete your request.")
        case _:
            logging.error(f"HTTP error occurred with status code {status_code}: {response.reason}")

def make_post_request(url, headers, data):
    """
    Invia una richiesta POST a un URL specificato con i dati forniti e gli header forniti.

    :param url: L'URL a cui inviare la richiesta POST.
    :param headers: Gli header della richiesta.
    :param data: I dati da inviare nella richiesta POST, come dizionario.
    :return: La risposta del server.
    """
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Ritorna requests.exceptions.HTTPError in caso di 4xx/5xx
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        logging.error(f"Response Status Code: {response.status_code}")
        logging.error(f"Response Headers: {response.headers}")
        logging.error(f"Response Body: {response.text}")
        handle_http_error(response)
    except Exception as err:
        logging.error(f"Other error occurred: {err}")

def make_delete_request(url, headers):
    """
    Invia una richiesta DELETE a un URL specificato con gli header forniti.

    :param url: L'URL a cui inviare la richiesta DELETE.
    :param headers: Gli header della richiesta.
    :return: La risposta del server.
    """
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        logging.error(f"Response Status Code: {response.status_code}")
        logging.error(f"Response Headers: {response.headers}")
        logging.error(f"Response Body: {response.text}")
        handle_http_error(response)
    except Exception as err:
        logging.error(f"Other error occurred: {err}")

def get_user_posts(user_id, headers):
    """
    Ottiene i post dell'utente tramite l'API di Mastodon.

    :param user_id: ID dell'utente di cui ottenere i post.
    :param headers: Gli header della richiesta.
    :return: Lista dei post dell'utente.
    """
    url = f"https://mastodon.social/api/v1/accounts/{user_id}/statuses"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        logging.error(f"Response Status Code: {response.status_code}")
        logging.error(f"Response Headers: {response.headers}")
        logging.error(f"Response Body: {response.text}")
        handle_http_error(response)
    except Exception as err:
        logging.error(f"Other error occurred: {err}")

def rate_limit(headers, endpoint_url):
    response = requests.get(endpoint_url, headers=headers)
    rate_limit = response.headers.get('X-RateLimit-Limit')
    rate_limit_remaining = response.headers.get('X-RateLimit-Remaining')
    rate_limit_reset = response.headers.get('X-RateLimit-Reset')
    
    # Converti la stringa ISO 8601 in un oggetto datetime
    reset_time = datetime.fromisoformat(rate_limit_reset.replace('Z', '+00:00'))

    # Calcola il tempo rimanente in secondi fino al reset
    time_until_reset = (reset_time - datetime.now(reset_time.tzinfo)).total_seconds()

    logging.info(f"Rate Limit: {rate_limit}")
    logging.info(f"Rate Limit Remaining: {rate_limit_remaining}")
    logging.info(f"Rate Limit Reset Time: {reset_time} (in {time_until_reset} seconds)")

def main():
    
    endpoint_url = "https://mastodon.social/api/v1/accounts/verify_credentials"
    user_id = ''  
    access_token = ''  # Assicurati di usare un token di accesso valido
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    rate_limit(headers=headers, endpoint_url=endpoint_url)
    
    while True:
        action = input("Vuoi pubblicare un nuovo post, eliminare un post esistente o uscire? (pubblica/elimina/exit): ").strip().lower()
        
        if action == 'exit':
            logging.info("Uscita dal programma.")
            break
        
        elif action == 'pubblica':
            url = "https://mastodon.social/api/v1/statuses"
            content = input("Inserisci il contenuto del post che vuoi creare: ")
            data = {
                "status": content
            }
            response = make_post_request(url, headers, data)
            if response:
                logging.info("Post pubblicato con successo.")
                logging.info(f"Response: {response}")  # Visualizza la risposta in formato JSON
                rate_limit(headers=headers, endpoint_url=endpoint_url)

        elif action == 'elimina':
            
            posts = get_user_posts(user_id, headers)
            
            if not posts:
                logging.info('Non ci sono post disponibili')
                continue

            for post in posts:
                logging.info(f"Post ID: {post['id']}, Content: {post['content']}")

            post_id = input("Inserisci l'ID del post che vuoi eliminare: ")
            url = f"https://mastodon.social/api/v1/statuses/{post_id}"
            response = make_delete_request(url, headers)
            if response:
                logging.info("Post eliminato con successo.")
                logging.info(f"Response: {response}")  # Visualizza la risposta in formato JSON
                rate_limit(headers=headers, endpoint_url=endpoint_url)
        else:
            logging.error("Azione non riconosciuta. Per favore scegli 'pubblica', 'elimina' o 'exit'.")

if __name__ == "__main__":
    main()
