import requests
import time
from datetime import datetime, timedelta

# URL dell'endpoint Mastodon
url = "https://mastodon.social/api/v1/accounts/verify_credentials"

# Headers per l'autenticazione
headers = {
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
}


# Effettua una richiesta GET
response = requests.get(url, headers=headers)

# Controlla gli headers relativi al rate limit
rate_limit = response.headers.get('X-RateLimit-Limit')
rate_limit_remaining = response.headers.get('X-RateLimit-Remaining')
rate_limit_reset = response.headers.get('X-RateLimit-Reset')

# Converti la stringa ISO 8601 in un oggetto datetime
reset_time = datetime.fromisoformat(rate_limit_reset.replace('Z', '+00:00'))

# Calcola il tempo rimanente in secondi fino al reset
time_until_reset = (reset_time - datetime.now(reset_time.tzinfo)).total_seconds()

print(f"Rate Limit: {rate_limit}")
print(f"Rate Limit Remaining: {rate_limit_remaining}")
print(f"Rate Limit Reset Time: {reset_time} (in {time_until_reset} seconds)")

# Controlla se il tempo rimanente è esattamente un minuto (60 secondi)
if time_until_reset == 60:
    print("Il limite di rate verrà resettato esattamente tra un minuto.")
else:
    print(f"Il limite di rate verrà resettato tra {time_until_reset} secondi.")

'''
Rate Limit: Indica il numero massimo di richieste che puoi 
effettuare nel periodo di tempo specificato (solitamente un minuto).

Rate Limit Remaining: Mostra quante richieste puoi ancora 
effettuare prima che venga raggiunto il limite.

Rate Limit Reset: Indica il momento in cui il contatore 
di rate limit verrà resettato (espresso come timestamp Unix).

'''
