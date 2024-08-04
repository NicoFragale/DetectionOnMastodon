import os 
import sys
import requests
import logging 
import datetime

# Aggiungi la directory superiore al percorso di ricerca dei moduli
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from credentials import user_id, access_token

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def rate_limit(headers, endpoint_url):
    response = requests.get(endpoint_url, headers=headers)
    rate_limit = response.headers.get('X-RateLimit-Limit')
    rate_limit_remaining = response.headers.get('X-RateLimit-Remaining')
    rate_limit_reset = response.headers.get('X-RateLimit-Reset')

    # Converti la stringa ISO 8601 in un oggetto datetime
    reset_time = datetime.datetime.fromisoformat(rate_limit_reset.replace('Z', '+00:00'))

    # Calcola il tempo rimanente in secondi fino al reset
    time_until_reset = (reset_time - datetime.datetime.now(reset_time.tzinfo)).total_seconds()

    logging.info(f"Rate Limit: {rate_limit}")
    logging.info(f"Rate Limit Remaining: {rate_limit_remaining}")
    logging.info(f"Rate Limit Reset Time: {reset_time} (in {time_until_reset} seconds)")

def request(headers):
    base_url = "https://mastodon.social"
    try:
        response = requests.get(f"{base_url}/api/v1/custom_emojis", headers=headers)
        response.raise_for_status()  # Ritorna requests.exceptions.HTTPError in caso di 4xx/5xx
        return response

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        logging.error(f"Response Status Code: {response.status_code}")
        logging.error(f"Response Headers: {response.headers}")
        logging.error(f"Response Body: {response.text}")
    except Exception as err:
        logging.error(f"Other error occurred: {err}")

def main():
    endpoint_url = '/api/v1/accounts/:id'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    rate_limit(headers, endpoint_url)
    response = request(headers)
    if response:
        logging.info(f"Response Status Code: {response.status_code}")
        logging.info(f"Response Body: {response.json()}")  # Assumendo che il corpo della risposta sia JSON
    rate_limit(headers, endpoint_url)

if __name__ == "__main__":
    main()
