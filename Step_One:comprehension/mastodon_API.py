import requests
import logging 

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_http_error(response):
    """
    Gestisce e stampa i dettagli dell'errore HTTP in base al codice di stato.

    :param response: Oggetto di risposta della richiesta HTTP.
    """
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



def make_post_request(url, access_token, data):
    """
    Invia una richiesta POST a un URL specificato con i dati forniti e l'access token di Mastodon.

    :param url: L'URL a cui inviare la richiesta POST.
    :param access_token: L'access token per l'autenticazione con l'API di Mastodon.
    :param data: I dati da inviare nella richiesta POST, come dizionario.
    :return: La risposta del server.
    """
    headers = {
        'Authorization': f'Bearer {access_token}', #autenticazione all'API per effettuare richiesta
        'Content-Type': 'application/json' #voglio postare il contenuto di un file JSON
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        # Con json=data,la libreria requests converte automaticamente il dizionario data in una stringa JSON 
        # e imposta l'header Content-Type a application/json.

        response.raise_for_status()  # ritorna requests.exceptions.HTTPError in caso di 4xx/5xx
        return response
    
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        logging.error(f"Response Status Code: {response.status_code}")
        logging.error(f"Response Headers: {response.headers}")
        logging.error(f"Response Body: {response.text}")
        handle_http_error(response)
    except Exception as err:
        logging.error(f"Other error occurred: {err}")

def main():
   
    url = "https://mastodon.social/api/v1/statuses" 
    access_token ='m4OkFhIdpe93ABgKoUOBuBfG7NboAM8dpiI1K27BCcc'  
    data = {
        "status": "Hello, Mastodon! I am posting using API"
    }
    
    response = make_post_request(url, access_token, data)
    
    if response:
        logging.info(response)


if __name__ == "__main__":
    main()
