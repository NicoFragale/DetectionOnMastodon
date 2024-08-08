import requests
import logging
from bs4 import BeautifulSoup
import sys
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from credentials import user_id, access_token, instance_url

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
    public_timeline_url = f"{instance_url}/api/v1/timelines/public"
    logging.info(f"Fetching posts from URL: {instance_url}")
    try:
        response = requests.get(public_timeline_url)
        logging.info(f"Response status code: {response.status_code}")
        response.raise_for_status()
        posts = response.json()
        number_post = 0 
        for post in posts:
            number_post += 1 
            html_content = '' + post['content'] + ''
            # Parsing del contenuto HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # Estrazione del testo
            text = soup.get_text()

            #print(post)
            logging.info(f"User: {post['account']['username']}")
            logging.info(f"Date: {post['created_at']}")
            logging.info(f"Content: {text}")
            print()
            print()
            print()
    
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        logging.error(f"Response Status Code: {response.status_code}")
        logging.error(f"Response Headers: {response.headers}")
        logging.error(f"Response Body: {response.text}")
        handle_http_error(response)
    except Exception as err:
        logging.error(f"Other error occurred: {err}")
        logging.error(f"Failed to retrieve posts: {response.status_code}")


def main():
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    get_user_posts(user_id, headers)

if __name__ == '__main__':
    main()