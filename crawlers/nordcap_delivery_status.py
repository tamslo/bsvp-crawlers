from crawlers.nordcap_base import NordcapBaseCrawler
from constants import NORDCAP_DELIVERY_STATUS_CRAWLER
from constants import DELIVERY_STATUS_PROPERTIES
from constants import DELIVERY_STATUS_AVAILABLE
from constants import DELIVERY_STATUS_SOON_AVAILABLE
from constants import DELIVERY_STATUS_UNAVAILABLE

class NordcapDeliveryStatusCrawler(NordcapBaseCrawler):
    name = NORDCAP_DELIVERY_STATUS_CRAWLER
    urls = [
        "https://www.nordcap.de/nordcap-shop/kuehltechnik/",
        "https://www.nordcap.de/nordcap-shop/cool-line/"
    ]
    header = DELIVERY_STATUS_PROPERTIES

    def get_page_product_urls(self, page):
        product_titles = page.find_all("a", "product--title")
        page_product_urls = list(map(
            lambda title: title["href"],
            product_titles
        ))
        return(page_product_urls)

    def get_product_information(self, product_page, product_url):
        article_number = product_page.find_all("span", "entry--content", itemprop = "sku")[0].text.strip()
        delivery_status_class = product_page.find_all("span", "delivery--text")[0]["class"][1]
        delivery_statuses = {
            "delivery--text-available": DELIVERY_STATUS_AVAILABLE,
            "delivery--text-more-is-coming": DELIVERY_STATUS_SOON_AVAILABLE,
            "delivery--text-not-available": DELIVERY_STATUS_UNAVAILABLE
        }
        if delivery_status_class in delivery_statuses:
            delivery_status = delivery_statuses[delivery_status_class]
        else:
            self.errors.append("Unbekannter Lieferstatus " + delivery_status_class + " in " + product_url)
            delivery_status = None
        return [ article_number, delivery_status ]
