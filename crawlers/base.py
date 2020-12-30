from bs4 import BeautifulSoup
import csv
import os
import urllib.request

class BaseCrawler:
    name = ""
    urls = []
    header = []
    csv_encoding = "utf-8"
    csv_delimiter = ";"
    errors = []
    logger = None

    def __init__(self, logger):
        self.logger = logger

    def get_page(self, base_url, page_number):
        self.__ensure_abstract_method("get_page")

    def get_total_pages(self, page):
        self.__ensure_abstract_method("get_total_pages")

    def get_page_product_urls(self, page):
        self.__ensure_abstract_method("get_page_product_urls")

    def get_product_information(self, product_page, product_url):
        self.__ensure_abstract_method("get_product_information")

    def __ensure_abstract_method(self, method_name):
        exception_text = "Die Methode '{}' muss von der Klasse implementiert "
        exception_text += "werden, die von NordcapCrawler erbt".format(method_name)
        raise Exception(exception_text)

    def get_soup(self, url):
        content = urllib.request.urlopen(url)
        read_content = content.read()
        soup = BeautifulSoup(read_content,'html.parser')
        return soup

    def get_product_urls(self, base_url):
        product_urls = []
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
        file_name = "{}.csv".format(self.name)
        for index, url in enumerate(self.urls):
            if index == 0:
                self.logger.log("Informationen über Kühlmöbel von {}".format(url), console_prefix = "---")
            elif index == len(self.urls) - 1:
                self.logger.log("und {} werden".format(url), console_prefix = "---")
            else:
                self.logger.log("und {}".format(url), console_prefix = "---")
        if len(self.urls) == 1:
            self.logger.log("werden in die Datei {} geschrieben".format(file_name), console_prefix = "---")
        else:
            self.logger.log("in die Datei {} geschrieben".format(file_name), console_prefix = "---")
        self.logger.log("")
        self.logger.log("Verfügbare Produkte werde gesammelt...", console_prefix = "---")
        product_urls = []
        for base_url in self.urls:
            product_urls = product_urls + self.get_product_urls(base_url)
        self.logger.log("{} Produkte gefunden".format(len(product_urls)), console_prefix = "---")
        with open(file_name, "w", newline = "", encoding = self.csv_encoding) as csv_file:
            csv_writer = csv.writer(csv_file, delimiter = self.csv_delimiter)
            csv_writer.writerow(self.header)
            product_number = 0
            self.logger.log("Produktinformationen werden gesammelt...", console_prefix = "---")
            for product_url in product_urls:
                product_number = product_number + 1
                self.logger.print_progress("Produkt", product_number, len(product_urls), console_prefix = "---")
                product_page = self.get_soup(product_url)
                product_information = self.get_product_information(product_page, product_url)
                csv_writer.writerow(product_information)
        if len(self.errors) == 0:
            self.logger.log("Vorgang abgeschlossen", console_prefix = "---")
        else:
            self.logger.log("Vorgang mit Fehlern abgeschlossen:", console_prefix = "---")
            for error in self.errors:
                self.logger.log("Fehler: " + error, console_prefix = "---")
        self.logger.log("")
