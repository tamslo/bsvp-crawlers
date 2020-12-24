from crawlers.base import BaseCrawler
from constants import RIVACOLD_DELIVERY_STATUS_CRAWLER
from constants import DELIVERY_STATUS_PROPERTIES
from constants import DELIVERY_STATUS_AVAILABLE
from constants import DELIVERY_STATUS_SOON_AVAILABLE

RIVACOLD_BASE_URL = "https://rivacold.de"

class RivacoldDeliveryStatusCrawler(BaseCrawler):
    name = RIVACOLD_DELIVERY_STATUS_CRAWLER
    urls = [
        "{}/de/Rivacold/artikel/Wandaggregat".format(RIVACOLD_BASE_URL),
        "{}/de/Rivacold/artikel/Deckenaggregat".format(RIVACOLD_BASE_URL),
        "{}/de/Rivacold/artikel/Splitaggregat".format(RIVACOLD_BASE_URL)
    ]
    header = DELIVERY_STATUS_PROPERTIES

    def get_page(self, base_url, page_number):
        page_url = "{}/{}".format(
            base_url,
            str(page_number)
        )
        return self.get_soup(page_url)

    def get_total_pages(self, page):
        indicator = page.find_all("a", "page-link")[-1]
        number = int(indicator["href"].split("/")[-1])
        return number

    def get_page_product_urls(self, page):
        product_rows = page.find_all("div", "cilistitem")
        page_product_urls = []
        for product_row in product_rows:
            product_title = product_row.find_all("h2")[0]
            product_url = product_title.find_all("a")[0]["href"]
            page_product_urls.append(RIVACOLD_BASE_URL + product_url)
        return page_product_urls

    def get_product_information(self, product_page, product_url):
        article_number = product_page.find_all("h1")[0].text.strip()
        article_number = article_number.split("-")[0]
        article_number = article_number.split("/")[0]
        article_number  = article_number[:10]
        article_number = "RC-{}".format(article_number)
        stock_number_text = product_page.find("div", { "id": "container2" }).find_all("p")[0].text
        stock_number = int(stock_number_text.split(" ")[-1].strip())
        if (stock_number > 0):
            delivery_status = DELIVERY_STATUS_AVAILABLE
        else:
            delivery_status = DELIVERY_STATUS_SOON_AVAILABLE
        return [ article_number, delivery_status ]
