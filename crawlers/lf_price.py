from crawlers.base import BaseCrawler
from constants import LF_PRICE_CRAWLER

class LfPriceCrawler(BaseCrawler):
    name = LF_PRICE_CRAWLER
    urls = ["https://b2bnet.lfspareparts724.com/RicercaRapida/Result?StringaDiRicerca="]
    needs_auth = True
    uses_input_csv = True

    def get_csv_item_url(self, csv_row, base_url):
        return "{}{}".format(base_url, csv_row["artikelnummer"])

    def get_auth_url(self):
        return "{}?codice=&uid={}&pwd={}&lingua=4".format(
                self.config["auth_url"],
                self.config["auth_user"],
                self.config["auth_password"])

    def __get_article_number_from_url(self, product_url):
        return product_url.replace(self.urls[0], "")

    def get_product_information(self, product_page, product_url):
        input_data = self._get_input_csv_data()
        article_number = self.__get_article_number_from_url(product_url)
        input_informations = [article for article in input_data if article["artikelnummer"] == article_number]
        if len(input_informations) > 1:
            self.logger.log("--- WARNUNG: {} Produkte mit Artikelnummer {} in Input CSV; wähle das erste".format( len(input_informations), article_number))
        if len(input_informations) == 0:
            self.errors.append("Kein Produkt mit Artikelnummer {} in Input CSV; Produkt wird übersprungen".format(article_number))
            return None
        input_information = input_informations[0]
        product_data = product_page.find_all("div", { "class": "product-data-panel" })
        if len(product_data) != 1:
            self.errors.append("Artikel {} hat mehr als einen div mit class='product-data-panel'".format(article_number))
            return None
        prodcuct_data_list = product_data[0].find_all("li")
        price_item = None
        for product_information in prodcuct_data_list:
            product_information_name = product_information.find("div", { "class": "data" }).text
            if product_information_name == 'Brutto Einzelpreis':
                price_item = product_information.find("strong")
                if len(price_item.find_all("del")) > 0:
                    price_item.find("del").decompose()
        if price_item is None:
            self.errors.append("Artikel {} hat keinen Brutto Einzelpreis".format(article_number))
            return None
        price = float(price_item.text.replace("€", "").replace(".", "").replace(",", ".").strip())
        input_information['listenpreis'] = price
        return input_information.values()