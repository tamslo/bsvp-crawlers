from bs4 import BeautifulSoup
import csv
import os
import requests

class BaseCrawler:
    name = ""
    urls = []
    header = []
    csv_encoding = "utf-8"
    csv_delimiter = ";"
    errors = []
    logger = None
    needs_auth = False
    uses_input_csv = False
    config = None

    def __init__(self, logger, config):
        self.logger = logger
        self.file_path = "{}.csv".format(self.name)
        output_paths = config["output_paths"]
        if self.name in output_paths:
            self.file_path = output_paths[self.name]
        if self.name in config:
            self.config = config[self.name]

    def get_page(self, base_url, page_number):
        self.__ensure_abstract_method("get_page")

    def get_total_pages(self, page):
        self.__ensure_abstract_method("get_total_pages")

    def get_page_product_urls(self, page):
        self.__ensure_abstract_method("get_page_product_urls")

    def get_product_information(self, product_page, product_url):
        self.__ensure_abstract_method("get_product_information")


    def get_csv_item_url(self, csv_row):
        self.__ensure_abstract_method("get_csv_item_url")

    def get_auth_url(self):
        self.__ensure_abstract_method("get_auth_url")

    def __ensure_abstract_method(self, method_name):
        exception_text = "Die Methode '{}' muss von der Klasse implementiert "
        exception_text += "werden, die von NordcapCrawler erbt".format(method_name)
        raise Exception(exception_text)

    def __test_config_field(self, config_field_name, consequence = None):
        error = None
        if self.config == None:
            error = "Config für '{}' fehlt".format(self.name)
        if not config_field_name in self.config:
            raise Exception("Config '{}' für '{}' fehlt".format(config_field_name, self.name))
        if error != None:
            if consequence != None:
                error = "{}; {}".format(error, consequence)
            raise Exception(error)

    def get_soup(self, url):
        if self.needs_auth:
            self.__test_config_field("auth_url")
            self.__test_config_field("auth_user")
            self.__test_config_field("auth_password")
            session = requests.Session()
            response = session.post(self.get_auth_url())
            content = session.get(url)
        else:
            content = requests.get(url)
        soup = BeautifulSoup(content.text,'html.parser')
        return soup

    def _get_input_csv_data(self):
        self.__test_config_field("input_csv_path")
        self.__test_config_field("input_csv_encoding")
        self.__test_config_field("input_csv_separator")
        csv_path = self.config["input_csv_path"]
        csv_encoding = self.config["input_csv_encoding"]
        csv_separator = self.config["input_csv_separator"]
        with open(csv_path, "r", encoding=csv_encoding) as input_csv_file:
            csv_reader = csv.DictReader(input_csv_file, delimiter=csv_separator)
            return list(csv_reader)

    def get_product_urls(self, base_url):
        product_urls = []
        if self.uses_input_csv:
            csv_reader = self._get_input_csv_data()
            for csv_row in csv_reader:
                product_urls.append(self.get_csv_item_url(csv_row, base_url))
        else:
            pages = self.get_pages(base_url)
            for page in pages:
                page_product_urls = self.get_page_product_urls(page)
                product_urls = product_urls + page_product_urls
        return product_urls

    def get_pages(self, base_url):
        pages = []
        first_page = self.get_page(base_url, 1)
        pages.append(first_page)
        total_pages = self.get_total_pages(first_page)
        for page_number in range(2, total_pages + 1):
            pages.append(self.get_page(base_url, page_number))
        return pages

    def run(self):
        self.logger.log("{} CRAWLER".format(self.name.replace("_", " ").upper()), console_prefix = "--")
        self.logger.log("")
        for index, url in enumerate(self.urls):
            if index == 0:
                self.logger.log("Informationen über Kühlmöbel von {}".format(url), console_prefix = "---")
            elif index == len(self.urls) - 1:
                self.logger.log("und {} werden".format(url), console_prefix = "---")
            else:
                self.logger.log("und {}".format(url), console_prefix = "---")
        if len(self.urls) == 1:
            self.logger.log("werden in die Datei {} geschrieben".format(self.file_path), console_prefix = "---")
        else:
            self.logger.log("in die Datei {} geschrieben".format(self.file_path), console_prefix = "---")
        self.logger.log("")
        self.logger.log("Verfügbare Produkte werde gesammelt...", console_prefix = "---")
        product_urls = []
        for base_url in self.urls:
            product_urls = product_urls + self.get_product_urls(base_url)
        self.logger.log("{} Produkte gefunden".format(len(product_urls)), console_prefix = "---")
        with open(self.file_path, "w", newline = "", encoding = self.csv_encoding) as csv_file:
            csv_writer = csv.writer(csv_file, delimiter = self.csv_delimiter)
            if self.uses_input_csv:
                input_data = self._get_input_csv_data()
                dict_from_csv = dict(input_data[0])
                self.header = list(dict_from_csv.keys())
            csv_writer.writerow(self.header)
            product_number = 0
            self.logger.log("Produktinformationen werden gesammelt...", console_prefix = "---")
            for product_url in product_urls:
                product_number = product_number + 1
                self.logger.print_progress("Produkt", product_number, len(product_urls), console_prefix = "---")
                product_page = self.get_soup(product_url)
                product_information = self.get_product_information(product_page, product_url)
                if product_information is not None:
                    csv_writer.writerow(product_information)
        if len(self.errors) == 0:
            self.logger.log("Vorgang abgeschlossen", console_prefix = "---")
        else:
            self.logger.log("Vorgang mit Fehlern abgeschlossen:", console_prefix = "---")
            for error in self.errors:
                self.logger.log("Fehler: " + error, console_prefix = "---")
        self.logger.log("")
