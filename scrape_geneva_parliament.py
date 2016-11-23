#!/usr/bin/env python
"""
Parses data from the Geneva parlament website."""

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from twisted.internet import reactor

PERSON_URL = "http://ge.ch/grandconseil/gc/depute/{}/"
PERSON_IDS = range(1, 2414)

CSS_MAP = {
    ".deputeInfo .deputeLastname::text": "last_name",
    ".deputeInfo .deputeFirstname::text": "first_name",

}

XPATH_MAP = {
    "normalize-space(//tr[td[.='Parti']]/td[2]/text())": "party",
}

LEGISLATURE_SELECTOR = "normalize-space(//tr[td[contains(.,'Législatur')]]/td[2]/div/text())"
INTERESTS_SELECTOR = "//tr[td[contains(.,'Liens d')]]/td[2]/div/text()"


class GenevaParlamentSpider(scrapy.Spider):
    name = "geneva_parlament"

    def start_requests(self):
        for i in PERSON_IDS:
            yield scrapy.Request(url=PERSON_URL.format(str(i)), callback=self.parse)

    def parse(self, response):
        data = {
            "interests": [],
        }

        for (selector, field_name) in CSS_MAP.items():
            data[field_name] = response.css(selector).extract_first().strip()

        for (selector, field_name) in XPATH_MAP.items():
            data[field_name] = response.xpath(selector).extract_first().strip()

        legislatures = response.xpath(LEGISLATURE_SELECTOR).extract()

        data["START_YEAR"] = int(legislatures[0].split("/")[0])
        data["END_YEAR"] = int(legislatures[-1].split("/")[-1])

        for interest in response.xpath(INTERESTS_SELECTOR).extract():
            interest = interest.strip().split(" - ")
            interest_dict = {"company": interest[0]}

            if len(interest) > 1:
                interest_dict["position"] = interest[1]

            data["interests"].append(interest_dict)

        return data


settings = {
    'FEED_FORMAT': 'json',
    'FEED_URI': 'stdout:',
}

process = CrawlerProcess(settings=Settings(settings))
process.crawl(GenevaParlamentSpider)
process.start()
