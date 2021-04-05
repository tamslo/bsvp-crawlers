import math
from crawlers.base import BaseCrawler
from constants import VIESSMANN_REPLACEMENTS_CRAWLER, VAT

VIESSMANN_BASE_URL = "https://shop.vkag.de"

class ViessmannReplacementsCrawler(BaseCrawler):
    name = VIESSMANN_REPLACEMENTS_CRAWLER
    urls = [
        "{}/kuhlzellen.html".format(VIESSMANN_BASE_URL),
        "{}/kuhlaggregate.html".format(VIESSMANN_BASE_URL),
        "{}/kuhlraumturen-luken.html".format(VIESSMANN_BASE_URL)
    ]
    header = ["Bestellnummer", "Nettopreis"]

    def get_page(self, base_url, page_number):
        page_url = "{}/{}".format(
            base_url,
           "?limit=all"
        )
        return self.get_soup(page_url)

    def get_total_pages(self, page):
        return 1

    def get_page_product_urls(self, page):
        product_rows = page.find_all("div", "list_product_headline")
        page_product_urls = []
        for product_row in product_rows:
            product_url = product_row.find_all("a")[0]["href"]
            page_product_urls.append(product_url)
        return page_product_urls

    def get_product_information(self, product_page, product_url):
        order_number = product_page.find("span", { "id": "sku" }).text
        brutto_price_text = product_page.find_all("span", "price")[0].text[:-2] # cut off " €"
        brutto_price = float(brutto_price_text.replace(".", "").replace(",", "."))
        netto_price = math.ceil(brutto_price / (1 + VAT))
        return [ order_number, netto_price ]
