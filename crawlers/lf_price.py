from crawlers.base import BaseCrawler
from constants import LF_PRICE_CRAWLER

class LfPriceCrawler(BaseCrawler):
    name = LF_PRICE_CRAWLER
    urls = ["https://b2bnet.lfspareparts724.com/RicercaRapida/Result?StringaDiRicerca="]

    def get_page(self, base_url, page_number):
        print("TODO: Implement")

    def get_total_pages(self, page):
        print("TODO: Implement")

    def get_page_product_urls(self, page):
        print("TODO: Implement")

    def get_product_information(self, product_page, product_url):
        print("TODO: Implement")