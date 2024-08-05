import scrapy


class MastodonSpiderSpider(scrapy.Spider):
    name = "mastodon_spider"
    allowed_domains = ["mastodon.social"]
    start_urls = ["https://mastodon.social"]

    def parse(self, response):
        pass
