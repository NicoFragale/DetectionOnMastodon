import requests

base_url = "https://mastodon.social"

# Visualizzare le informazioni generali sull'istanza
instance_info = requests.get(f"{base_url}/api/v1/instance")
print(instance_info.json())

# Visualizzare i peer dell'istanza
instance_peers = requests.get(f"{base_url}/api/v1/instance/peers")
print(instance_peers.json())

# Visualizzare l'attività settimanale dell'istanza
instance_activity = requests.get(f"{base_url}/api/v1/instance/activity")
print(instance_activity.json())



# Elencare tutti gli emoji personalizzati disponibili
custom_emojis = requests.get(f"{base_url}/api/v1/custom_emojis")
print(custom_emojis.json())


# Visualizzare una directory di tutti i profili disponibili
directory = requests.get(f"{base_url}/api/v1/directory")
print(directory.json())

# Visualizzare gli hashtag attualmente in tendenza
trends = requests.get(f"{base_url}/api/v1/trends")
print(trends.json())
