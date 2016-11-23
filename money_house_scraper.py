from random import random
import time

from lxml import html
from selenium import webdriver

SEARCH_URL = "https://www.moneyhouse.ch/fr/search?q={}&status=1&tab=companies"

# URL suffix to obtain a list of managers
MANAGEMENT_URL = "/management?activeOnly=true&page=0"

# Message to look for if suspecting to be throttled
THROTTLE_MSG = "Pardon Our Interruption"

dcap = webdriver.DesiredCapabilities.PHANTOMJS
dcap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"
dcap["phantomjs.page.customHeaders.Accept-Language"] = "en-US,en;q=0.8,fr;q=0.6,it;q=0.4"
dcap["phantomjs.page.customHeaders.Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
dcap["phantomjs.page.customHeaders.Connection"] = "keep-alive"

driver = webdriver.PhantomJS(desired_capabilities=dcap)


def check_throttle():
    if THROTTLE_MSG in driver.page_source:
        raise RuntimeError("Throttled!")


def random_sleep():
    time.sleep(0.2 + random())


def scrape_company(name):
    driver.get(SEARCH_URL.format(name))
    tree = html.fromstring(driver.page_source)
    results = tree.xpath("//tbody[@class='js-search-result-item']//a/@href")

    if not results:
        return None

    company_url = "https://www.moneyhouse.ch/" + results[0]
    random_sleep()

    driver.get(company_url+MANAGEMENT_URL)




    # do the search request
    # pick the first result
    # scrape
	return
