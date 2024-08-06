import logging
logging.getLogger('scrapy').setLevel(logging.DEBUG)
import scrapy

class MastodonSpider(scrapy.Spider):
    name = 'spidy'
    allowed_domains = ['mastodon.social']
    start_urls = ['https://mastodon.social/@Range_']

    def parse(self, response):
        # Estrai il contenuto del meta tag description
        description_content = response.xpath("//meta[@name='description']/@content").get()

        if description_content:
            # Parso il contenuto per estrarre i dati
            parts = description_content.split(' · ')
            post_info = parts[0].split(', ')
            posts = post_info[0].split(' ')[0]
            following = post_info[1].split(' ')[0]
            followers = post_info[2].split(' ')[0]
            bio = parts[1] if len(parts) > 1 else ''

            yield {
                'posts': posts,
                'following': following,
                'followers': followers,
                'bio': bio,
            }

    def is_disallowed(self, url):
        # Lista delle direttive disallow da robots.txt
        disallowed_paths = [
            '/media_proxy/',
            '/interact/'
        ]

        
        return any(url.startswith(path) for path in disallowed_paths)
    
# Configura il logging
logging.basicConfig(level=logging.INFO)

# Run the spider with: scrapy runspider mastodon_spider.py


'''
YIELD:
yield è una keyword in Python che viene utilizzata per trasformare una funzione in un generatore. 
Un generatore è un tipo speciale di funzione che restituisce un oggetto su cui puoi iterare (come una lista), 
ma fa questo in modo "pigro" (lazily), il che significa che produce gli elementi uno alla volta e solo quando richiesto.

'''

'''Questa riga verifica se l'URL inizia con uno dei percorsi disallowati. 
        Se sì, ritorna True, altrimenti False. 
        Il metodo startswith controlla se una stringa inizia con un determinato prefisso. 
        La funzione any ritorna True se almeno una delle condizioni è vera.
'''



'''parse viene chiamato automaticamente da Scrapy 
    per gestire le risposte dalle richieste iniziali 
    definite in start_urls. 
    Il parametro response contiene il contenuto della pagina web scaricata.'''