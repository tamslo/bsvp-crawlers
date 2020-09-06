from bs4 import BeautifulSoup
import csv
import os
import time
import urllib.request

BASE_URL = "https://www.nordcap-outlet.de/kuehltechnik/"
CSV_ENCODING = "utf-8"
CSV_DELIMITER = ";"

errors = []

def get_soup(url):
    content = urllib.request.urlopen(url)
    read_content = content.read()
    soup = BeautifulSoup(read_content,'html.parser')
    return soup

def get_page(page_number):
    ordering = "1" # Erscheinungsdatum
    items_per_page = "80"
    page_url = "{}?p={}&o={}&n={}".format(
        BASE_URL,
        str(page_number),
        ordering,
        items_per_page
    )
    return get_soup(page_url)

def get_total_pages(page):
    indicator = page.find_all("span", "paging--display")[0]
    number = int(indicator.find_all("strong")[0].text)
    return number

def get_pages():
    pages = []
    first_page = get_page(1)
    pages.append(first_page)
    total_pages = get_total_pages(first_page)
    for page_number in range(2, total_pages + 1):
        pages.append(get_page(page_number))
    return(pages)

def get_product_urls():
    product_urls = []
    pages = get_pages()
    for page in pages:
        product_buttons = page.find_all("div", "product--detail-btn")
        page_product_urls = list(map(
            lambda button: button.find_all("a")[0]["href"],
            product_buttons
        ))
        product_urls = product_urls + page_product_urls
    return product_urls

def get_product_information(product_url):
    product_page = get_soup(product_url)
    price = product_page.find_all("span", "price--content")[0].text[0:-4].strip()
    outlet_code = product_page.find_all("span", "entry--content", itemprop = "sku")[0].text.strip()
    article_number = product_page.find_all("span", "entry--content", itemprop = "artikelnummer")[0].text.strip()
    article_name = "Nordcap " + product_page.find_all("h1", "product--title")[0].text.strip()
    article_type = product_page.find_all("span", "entry--content", itemprop = "geraeteart")[0].text.strip()
    warranty = product_page.find_all("span", "entry--content", itemprop = "seriennummer")[-1].text.strip()

    def get_description(product_page):
        def get_main_parts(all_parts):
            main_content_indicator = "gerät"
            return [part for part in all_parts if main_content_indicator in part.text.lower()]

        result_parts = []
        description = product_page.find_all("div", "product--description")[0]
        strong_parts = description.find_all("strong")
        description_parts = description.find_all("p")
        possible_main_parts = get_main_parts(description_parts)

        main_description = ""
        if len(strong_parts) > 0:
            main_description = strong_parts[0].text
        elif len(possible_main_parts) > 0:
            if len(possible_main_parts[0]) > 1:
                main_description = possible_main_parts[0].get_text(" ")
            else:
                main_description = possible_main_parts[0].text
        else:
            errors.append("Keine Beschreibung gefunden für " + product_url)
        result_parts.append(main_description)
        # TODO: Add damages (everything after index of main_description?)
        result = ", ".join(result_parts)
        return result

    def get_image_urls(page_number):
        thumbnail_list = product_page.find_all("div", "image-slider--thumbnails-slide")
        if (len(thumbnail_list) > 0):
            thumbnails = thumbnail_list[0].find_all("a")
            image_urls = list(map(lambda thumbnail: thumbnail["href"], thumbnails))
        else:
            image_urls = [product_page.find_all("span", "image--element")[0]["data-img-original"]]
        return image_urls

    def get_image_url(image_urls, number):
        return image_urls[number - 1] if len(image_urls) >= number else None

    image_urls = get_image_urls(product_page)

    #return [get_description(product_page), product_url]
    return [
        product_url,
        price,
        outlet_code,
        article_number,
        article_name,
        article_type,
        warranty,
        get_description(product_page),
        get_image_url(image_urls, 1),
        get_image_url(image_urls, 2),
        get_image_url(image_urls, 3),
        get_image_url(image_urls, 4),
        get_image_url(image_urls, 5)
    ]

def get_header():
    #return(["description", "url"])
    return ([
        "URL",
        "Preis",
        "OutletCode",
        "Artikelnummer",
        "Artikelname",
        "Geräteart",
        "Gewährleistung",
        "Bescheibung",
        "Bild1",
        "Bild2",
        "Bild3",
        "Bild4",
        "Bild5"
    ])

def main():
    print("")
    print("-- NORDCAP OUTLET CRAWLER")
    print("-- © 2020 Tamara Slosarek")
    print("")
    file_name = "nordcap_outlet_{}.csv".format(time.strftime("%Y%m%dT%H%M%S"))
    print("-- NordCap Outlet Kühlmöbel von {} werden in die Datei".format(BASE_URL))
    print("-- {} geschrieben".format(file_name))
    print("")
    print("-- Verfügbare Produkte werde gesammelt...")
    product_urls = get_product_urls()
    print("-- {} Produkte gefunden".format(len(product_urls)))
    with open(file_name, "w", newline = "", encoding = CSV_ENCODING) as csv_file:
        csv_writer = csv.writer(csv_file, delimiter = CSV_DELIMITER)
        csv_writer.writerow(get_header())
        product_number = 0
        print("")
        print("-- Produktinformationen werden gesammelt...")
        for product_url in product_urls:
            product_number = product_number + 1
            print("-- Produkt {} von {}\r".format(product_number, len(product_urls)), end = "")
            csv_writer.writerow(get_product_information(product_url))
    if len(errors) == 0:
        print("-- Vorgang abgeschlossen")
    else:
        print("-- Vorgang mit Fehlern abgeschlossen:")
        for error in errors:
            print("-- Fehler: " + error)
    print("")

if __name__ == "__main__":
    main()
