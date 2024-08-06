#framework in uso per il crawling
import scrapy

#scrapy.Spider è il ragno che effettua il crawling
class MastodonSpiderSpider(scrapy.Spider):
    name = "mastodon_spider" # nome del ragno
    allowed_domains = ["mastodon.social"] # lista di domini che il nostro spider è autorizzato a visitare
    start_urls = ["https://mastodon.social"] # da dove inizia il crawling

    # dobbiamo rispettare le direttive di robots.txt
    custom_settings = {
        'ROBOTSTXT_OBEY': True,
    }


    '''parse viene chiamato automaticamente da Scrapy 
    per gestire le risposte dalle richieste iniziali 
    definite in start_urls. 
    Il parametro response contiene il contenuto della pagina web scaricata.'''

    def parse(self, response):

        # Trova tutti i link nella pagina 
        links = response.css('a::attr(href)').getall() 
        '''response.css estra tutti i link (<'a'>) in pagina usando selettori 'css' per trovare elementi nel documento HTML. 
        ::attr(href) estrae l'attributo href (l'URL) di ogni link. 
        getall() restituisce una lista di tutti i link trovati.
        '''
        for link in links:
            if not self.is_disallowed(link): # se siamo autorizzati a effettuare crawling
                yield response.follow(link, self.parse_page)
                '''
                response.follow è un metodo fornito da Scrapy che segue un link e restituisce un oggetto Request.
                'yield' definisce un generatore, ovvero una funzione che restituisce un iteratore che genera una sequenza di valori.
                'yield' consente allo spider di generare più richieste in modo incrementale senza doverle memorizzare tutte in memoria contemporaneamente.
                '''
    def parse_page(self, response): # Il parametro response contiene il contenuto della pagina web scaricata.
        
        # Esegui la logica di scraping per ogni pagina
        self.log(f'Visiting {response.url}')
        
        # Esempio di estrazione dati
        page_title = response.css('title::text').get()
        self.log(f'Page title: {page_title}')

    def is_disallowed(self, url):
        # Lista delle direttive disallow da robots.txt
        disallowed_paths = [
            '/media_proxy/',
            '/interact/'
        ]

        '''
        Questa riga verifica se l'URL inizia con uno dei percorsi disallowati. 
        Se sì, ritorna True, altrimenti False. 
        Il metodo startswith controlla se una stringa inizia con un determinato prefisso. 
        La funzione any ritorna True se almeno una delle condizioni è vera.
        '''
        return any(url.startswith(path) for path in disallowed_paths)
    

'''
YIELD:
yield è una keyword in Python che viene utilizzata per trasformare una funzione in un generatore. 
Un generatore è un tipo speciale di funzione che restituisce un oggetto su cui puoi iterare (come una lista), 
ma fa questo in modo "pigro" (lazily), il che significa che produce gli elementi uno alla volta e solo quando richiesto.


'''
