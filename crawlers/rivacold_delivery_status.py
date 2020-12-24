from crawlers.base import BaseCrawler
from constants import RIVACOLD_DELIVERY_STATUS_CRAWLER, DELIVERY_STATUS_PROPERTIES

class RivacoldDeliveryStatusCrawler(BaseCrawler):
    name = RIVACOLD_DELIVERY_STATUS_CRAWLER
    urls = [
        "https://rivacold.de/de/Rivacold/artikel/Wandaggregat/1",
        "https://rivacold.de/de/Rivacold/artikel/Deckenaggregat/1",
        "https://rivacold.de/de/Rivacold/artikel/Splitaggregat/1"
    ]
    header = DELIVERY_STATUS_PROPERTIES

    def get_total_pages(self, page):
        # indicator = page.find_all("span", "paging--display")[0]
        # number = int(indicator.find_all("strong")[0].text)
        # return(number)

    def get_page(self, base_url, page_number):
        # ordering = "1" # Erscheinungsdatum
        # items_per_page = "80"
        # page_url = "{}?p={}&o={}&n={}".format(
        #     base_url,
        #     str(page_number),
        #     ordering,
        #     items_per_page
        # )
        # return self.get_soup(page_url)

    def get_page_product_urls(self, page):
        # product_titles = page.find_all("a", "product--title")
        # page_product_urls = list(map(
        #     lambda title: title["href"],
        #     product_titles
        # ))
        # return(page_product_urls)

    def get_product_information(self, product_page, product_url):
        # article_number = product_page.find_all("span", "entry--content", itemprop = "sku")[0].text.strip()
        # delivery_status_class = product_page.find_all("span", "delivery--text")[0]["class"][1]
        # delivery_statuses = {
        #     "delivery--text-available": 1,
        #     "delivery--text-more-is-coming": 4,
        #     "delivery--text-not-available": 5
        # }
        # if delivery_status_class in delivery_statuses:
        #     delivery_status = delivery_statuses[delivery_status_class]
        # else:
        #     self.errors.append("Unbekannter Lieferstatus " + delivery_status_class + " in " + product_url)
        #     delivery_status = None
        # return [ article_number, delivery_status ]
