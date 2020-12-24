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
        print("-- {} CRAWLER".format(self.name.replace("_", " ").upper()))
        print("")
        file_name = "{}.csv".format(self.name)
        print("--- Informationen über Kühlmöbel von {} werden in die Datei".format(" und ".join(self.urls)))
        print("--- {} geschrieben".format(file_name))
        print("")
        print("--- Verfügbare Produkte werde gesammelt...")
        product_urls = []
        for base_url in self.urls:
            product_urls = product_urls + self.get_product_urls(base_url)
        print("--- {} Produkte gefunden".format(len(product_urls)))
        with open(file_name, "w", newline = "", encoding = self.csv_encoding) as csv_file:
            csv_writer = csv.writer(csv_file, delimiter = self.csv_delimiter)
            csv_writer.writerow(self.header)
            product_number = 0
            print("")
            print("--- Produktinformationen werden gesammelt...")
            for product_url in product_urls:
                product_number = product_number + 1
                print("--- Produkt {} von {}\r".format(product_number, len(product_urls)), end = "")
                product_page = self.get_soup(product_url)
                product_information = self.get_product_information(product_page, product_url)
                csv_writer.writerow(product_information)
        if len(self.errors) == 0:
            print("--- Vorgang abgeschlossen")
        else:
            print("--- Vorgang mit Fehlern abgeschlossen:")
            for error in self.errors:
                print("--- Fehler: " + error)
        print("")
