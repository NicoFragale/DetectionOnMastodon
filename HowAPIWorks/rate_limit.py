import os 
import sys
import requests
import logging 
import datetime

# Aggiungi la directory superiore al percorso di ricerca dei moduli
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from credentials import user_id, access_token

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def rate_limit(headers, endpoint_url):
    try:
        response = requests.get(endpoint_url, headers=headers)
        response.raise_for_status()  # Verifica se la richiesta ha avuto successo

        # Stampa tutti gli header della risposta per debug
        logging.info(f"Response Headers: {response.headers}")

        rate_limit = response.headers.get('X-RateLimit-Limit')
        rate_limit_remaining = response.headers.get('X-RateLimit-Remaining')
        rate_limit_reset = response.headers.get('X-RateLimit-Reset')

        if rate_limit and rate_limit_remaining and rate_limit_reset:
            # Converti la stringa ISO 8601 in un oggetto datetime
            reset_time = datetime.datetime.fromisoformat(rate_limit_reset.replace('Z', '+00:00'))

            # Calcola il tempo rimanente in secondi fino al reset
            time_until_reset = (reset_time - datetime.datetime.now(reset_time.tzinfo)).total_seconds()

            logging.info(f"Rate Limit: {rate_limit}")
            logging.info(f"Rate Limit Remaining: {rate_limit_remaining}")
            logging.info(f"Rate Limit Reset Time: {reset_time} (in {time_until_reset} seconds)")
        else:
            logging.info("Rate limit headers not present in the response.")
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"Other error occurred: {err}")

def main():
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Endpoint per verificare le credenziali dell'account
    verify_credentials_url = 'https://mastodon.social/api/v1/accounts/verify_credentials'
    rate_limit(headers, verify_credentials_url)

    '''# Endpoint per caricare i media
    upload_media_url = 'https://mastodon.social/api/v1/media'
    rate_limit(headers, upload_media_url)'''

    # Endpoint per cancellare i post
    delete_status_url = 'https://mastodon.social/api/v1/statuses/1'  # Cambia "1" con un ID valido per test
    rate_limit(headers, delete_status_url)

if __name__ == "__main__":
    main()
