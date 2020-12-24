from bs4 import BeautifulSoup
from crawlers.base import BaseCrawler
import csv
import os
import urllib.request

class NordcapBaseCrawler(BaseCrawler):
    def get_page(self, base_url, page_number):
        ordering = "1" # Erscheinungsdatum
        items_per_page = "80"
        page_url = "{}?p={}&o={}&n={}".format(
            base_url,
            str(page_number),
            ordering,
            items_per_page
        )
        return self.get_soup(page_url)

    def get_total_pages(self, page):
        indicator = page.find_all("span", "paging--display")[0]
        number = int(indicator.find_all("strong")[0].text)
        return(number)
