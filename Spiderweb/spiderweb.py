import requests
import logging
import time
from datetime import datetime, timedelta
import sys
import os
from bs4 import BeautifulSoup
# Aggiungi la directory superiore al percorso di ricerca dei moduli
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from credentials import user_id, access_token, endpoint_url

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


def get_user_posts(user_id, headers):
    """
    Ottiene i post dell'utente tramite l'API di Mastodon.

    :param user_id: ID dell'utente di cui ottenere i post.
    :param headers: Gli header della richiesta.
    :return: Lista dei post dell'utente.
    """
    url = f"https://mastodon.social/api/v1/accounts/{user_id}/statuses"
    logging.info(f"Fetching posts from URL: {url}")
    try:
        response = requests.get(url, headers=headers)
        logging.info(f"Response status code: {response.status_code}")
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


def main():
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    posts = get_user_posts(user_id, headers)

    for post in posts:
        html_content = '' + post['content'] + ''
        # Parsing del contenuto HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Estrazione del testo
        text = soup.get_text()
    
        logging.info(f"Date: {post['created_at']}, Content: {text}")
        print()
        print()
        print()

if __name__ == "__main__":
    main()