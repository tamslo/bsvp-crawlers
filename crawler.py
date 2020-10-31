import argparse
import time

from constants import OUTLET_CRAWLER, DELIVERY_STATUS_CRAWLER
from crawlers.outlet import OutletCrawler
from crawlers.delivery_status import DeliveryStatusCrawler

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--{}".format(OUTLET_CRAWLER), action="store_true")
parser.add_argument("-d", "--{}".format(DELIVERY_STATUS_CRAWLER), action="store_true")

crawlers = {
    OUTLET_CRAWLER: OutletCrawler,
    DELIVERY_STATUS_CRAWLER: DeliveryStatusCrawler
}

def main():
    args = parser.parse_args()
    selected_crawlers = []
    for crawler, selected in args.__dict__.items():
        if (selected):
            selected_crawlers.append(crawler)
    if len(selected_crawlers) == 0:
        selected_crawlers = crawlers.keys()

    print("")
    print("-- NORDCAP CRAWLERS")
    print("-- © {} Tamara Slosarek".format(time.strftime("%Y")))
    print("")

    for crawler in selected_crawlers:
        Crawler = crawlers[crawler]
        Crawler().run()


if __name__ == "__main__":
    main()
