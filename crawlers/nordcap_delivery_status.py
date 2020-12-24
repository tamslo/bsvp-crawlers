from crawlers.nordcap_base import NordcapBaseCrawler
from constants import NORDCAP_DELIVERY_STATUS_CRAWLER

class NordcapDeliveryStatusCrawler(NordcapBaseCrawler):
    name = NORDCAP_DELIVERY_STATUS_CRAWLER
    urls = [
        "https://www.nordcap.de/nordcap-shop/kuehltechnik/",
        "https://www.nordcap.de/nordcap-shop/cool-line/"
    ]
    header = [ "Artikelnummer", "Lieferstatus" ]

    def get_page_product_urls(self, page):
        product_titles = page.find_all("a", "product--title")
        page_product_urls = list(map(
            lambda title: title["href"],
            product_titles
        ))
        return(page_product_urls)

    def get_product_information(self, product_url):
        product_page = self.get_soup(product_url)
        article_number = product_page.find_all("span", "entry--content", itemprop = "sku")[0].text.strip()
        delivery_status_class = product_page.find_all("span", "delivery--text")[0]["class"][1]
        delivery_statuses = {
            "delivery--text-available": 1,
            "delivery--text-more-is-coming": 4,
            "delivery--text-not-available": 5
        }
        if delivery_status_class in delivery_statuses:
            delivery_status = delivery_statuses[delivery_status_class]
        else:
            self.errors.append("Unbekannter Lieferstatus " + delivery_status_class + " in " + product_url)
            delivery_status = None
        return [ article_number, delivery_status ]
