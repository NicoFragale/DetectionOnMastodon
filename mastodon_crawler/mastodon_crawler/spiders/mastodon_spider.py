import logging
from scrapy.utils.log import configure_logging
import scrapy

# Configura il logging per Scrapy
configure_logging(install_root_handler=False)
logging.basicConfig(
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    level=logging.INFO
)
logging.getLogger('scrapy').setLevel(logging.INFO)

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

# Run the spider with: scrapy runspider mastodon_spider.py
