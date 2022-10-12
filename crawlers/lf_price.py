from crawlers.base import BaseCrawler
from constants import LF_PRICE_CRAWLER

class LfPriceCrawler(BaseCrawler):
    name = LF_PRICE_CRAWLER
    urls = ["https://b2bnet.lfspareparts724.com/RicercaRapida/Result?StringaDiRicerca="]
    needs_auth = True
    uses_input_csv = True

    def get_csv_item_url(self, csv_row, base_url):
        return "{}{}".format(base_url, csv_row["artikelnummer"])

    def __get_article_number_from_url(self, product_url):
        return product_url.replace(self.urls[0], "")

    def get_product_information(self, product_page, product_url):
        input_data = self._get_input_csv_data()
        article_number = self.__get_article_number_from_url(product_url)
        with open(article_number + ".html", "w") as test_file:
            test_file.write(str(product_page))
        input_informations = [article for article in input_data if article["artikelnummer"] == article_number]
        if len(input_informations) > 1:
            self.logger.log("--- WARNUNG: {} Produkte mit Artikelnummer {} in Input CSV; wähle das erste".format( len(input_informations), article_number))
        if len(input_informations) == 0:
            self.errors.append("Kein Produkt mit Artikelnummer {} in Input CSV; Produkt wird übersprungen".format(article_number))
            return None
        input_information = input_informations[0]
        # TODO: Get 'Brutto Einzelpreis'
        return input_information.values()