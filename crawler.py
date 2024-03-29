import argparse
import time
import traceback

from config import get_config
from constants import NORDCAP_OUTLET_CRAWLER
from constants import NORDCAP_DELIVERY_STATUS_CRAWLER
from constants import RIVACOLD_DELIVERY_STATUS_CRAWLER
from constants import VIESSMANN_REPLACEMENTS_CRAWLER
from constants import LF_PRICE_CRAWLER
from crawlers.nordcap_outlet import NordcapOutletCrawler
from crawlers.nordcap_delivery_status import NordcapDeliveryStatusCrawler
from crawlers.rivacold_delivery_status import RivacoldDeliveryStatusCrawler
from crawlers.viessmann_replacements import ViessmannReplacementsCrawler
from crawlers.lf_price import LfPriceCrawler
from logger import Logger

parser = argparse.ArgumentParser()
parser.add_argument("-no", "--{}".format(NORDCAP_OUTLET_CRAWLER), action="store_true")
parser.add_argument("-nd", "--{}".format(NORDCAP_DELIVERY_STATUS_CRAWLER), action="store_true")
parser.add_argument("-rd", "--{}".format(RIVACOLD_DELIVERY_STATUS_CRAWLER), action="store_true")
parser.add_argument("-vr", "--{}".format(VIESSMANN_REPLACEMENTS_CRAWLER), action="store_true")
parser.add_argument("-lp", "--{}".format(LF_PRICE_CRAWLER), action="store_true")

default_crawlers = [
    NORDCAP_OUTLET_CRAWLER,
    NORDCAP_DELIVERY_STATUS_CRAWLER,
    RIVACOLD_DELIVERY_STATUS_CRAWLER,
    LF_PRICE_CRAWLER,
]

crawlers = {
    NORDCAP_OUTLET_CRAWLER: NordcapOutletCrawler,
    NORDCAP_DELIVERY_STATUS_CRAWLER: NordcapDeliveryStatusCrawler,
    RIVACOLD_DELIVERY_STATUS_CRAWLER: RivacoldDeliveryStatusCrawler,
    VIESSMANN_REPLACEMENTS_CRAWLER: ViessmannReplacementsCrawler,
    LF_PRICE_CRAWLER: LfPriceCrawler,
}

def main():
    args = parser.parse_args()
    selected_crawlers = []
    for crawler, selected in args.__dict__.items():
        if (selected):
            selected_crawlers.append(crawler)
    if len(selected_crawlers) == 0:
        selected_crawlers = default_crawlers

    config = get_config()

    logger = Logger()
    logger.log("")
    logger.log("BSVP CRAWLERS", console_prefix = "--")
    logger.log("© {} Tamara Slosarek".format(time.strftime("%Y")), console_prefix = "--")
    logger.log("")

    for crawler in selected_crawlers:
        Crawler = crawlers[crawler]
        try:
            Crawler(logger, config).run()
        except Exception as exception:
            logger.log("Es ist ein Fehler aufgetreten:", console_prefix = "---")
            logger.log(traceback.format_exc())


if __name__ == "__main__":
    main()
