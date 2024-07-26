import requests
import sys

# Configurazione API
API_BASE_URL = 'https://mastodon.example'  # Sostituisci con l'URL della tua istanza Mastodon
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'  # Inserisci il tuo token di accesso

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

def make_request(endpoint):
    """Effettua una richiesta all'endpoint API specificato e restituisce la risposta JSON."""
    url = f"{API_BASE_URL}{endpoint}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Errore {response.status_code}: {response.text}")
        return None

def get_public_toots():
    """Recupera e stampa i post pubblici."""
    endpoint = '/api/v1/timelines/public'
    data = make_request(endpoint)
    if data:
        for post in data:
            print(f"Post ID: {post['id']}")
            print(f"Contenuto: {post['content']}")
            print("-" * 80)

def get_user_details(user_id):
    """Recupera e stampa i dettagli di un utente specifico."""
    endpoint = f'/api/v1/accounts/{user_id}'
    data = make_request(endpoint)
    if data:
        print(f"Username: {data['username']}")
        print(f"Bio: {data['note']}")
        print(f"Followers: {data['followers_count']}")
        print(f"Following: {data['following_count']}")
        print("-" * 80)

def main():
    if len(sys.argv) < 2:
        print("Uso: python mastodon_api.py <comando> [<parametri>]")
        print("Comandi disponibili: public_toots, user_details")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'public_toots':
        get_public_toots()
    elif command == 'user_details':
        if len(sys.argv) != 3:
            print("Uso: python mastodon_api.py user_details <user_id>")
            sys.exit(1)
        user_id = sys.argv[2]
        get_user_details(user_id)
    else:
        print(f"Comando sconosciuto: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
