from crawlers.nordcap_base import NordcapBaseCrawler
from constants import OUTLET_CRAWLER

class OutletCrawler(NordcapBaseCrawler):
    name = OUTLET_CRAWLER
    urls = ["https://www.nordcap-outlet.de/kuehltechnik/"]
    header = [
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
    ]

    def get_page_product_urls(self, page):
        product_buttons = page.find_all("div", "product--detail-btn")
        page_product_urls = list(map(
            lambda button: button.find_all("a")[0]["href"],
            product_buttons
        ))
        return(page_product_urls)

    def get_product_information(self, product_url):
        product_page = self._get_soup(product_url)
        price = product_page.find_all("span", "price--content")[0].text[0:-4].strip()
        outlet_code = product_page.find_all("span", "entry--content", itemprop = "sku")[0].text.strip()
        article_number = product_page.find_all("span", "entry--content", itemprop = "artikelnummer")[0].text.strip()
        article_name = product_page.find_all("h1", "product--title")[0].text.strip()
        article_type = product_page.find_all("span", "entry--content", itemprop = "geraeteart")[0].text.strip()
        # Warranty items called "seriennummer" on outlet page; need to differentiate
        serial_number_items = product_page.find_all("span", "entry--content", itemprop = "seriennummer")
        warranty = serial_number_items[-1].text.strip()
        if (len(serial_number_items) > 1):
            serial_number = serial_number_items[0].text.strip()
            outlet_code = "{} / {}".format(outlet_code, serial_number)

        def get_description(product_page):
            def get_main_parts(all_parts):
                main_content_indicator = "gerät"
                return [part for part in all_parts if main_content_indicator in part.text.lower()]

            def get_main_description_index(description_parts, part):
                main_description_index = -1
                index = -1
                for description_part in description_parts:
                    index = index + 1
                    if (description_part.text == part.text):
                        main_description_index = index
                        break
                return main_description_index

            def get_further_description(description, description_parts, main_description_part):
                main_description_index = get_main_description_index(description_parts, main_description_part)
                further_parts = list(map(
                    lambda further_part: further_part.get_text(", "),
                    description_parts[main_description_index + 1:]
                ))
                damage_list = description.find_all("ul")
                if len(damage_list) > 0:
                    damage_list = list(map(
                        lambda list_item: list_item.get_text(),
                        damage_list[0].find_all("li")
                    ))
                return further_parts + damage_list

            description = product_page.find_all("div", "product--description")[0]
            strong_parts = description.find_all("strong")
            description_parts = description.find_all("p")
            possible_main_parts = get_main_parts(description_parts)

            if len(strong_parts) > 0:
                main_description_part = strong_parts[0]
            elif len(possible_main_parts) > 0:
                main_description_part = possible_main_parts[0]
            else:
                self.errors.append("Keine Beschreibung gefunden für " + product_url)
                return None

            main_description = main_description_part.get_text(" ").strip()
            result = [ main_description ] + get_further_description(description, description_parts, main_description_part)
            result =  ", ".join(result)
            result = result.strip()
            if result.endswith(","): result = result[0:-1]
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

        return [
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
