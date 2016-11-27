import time

from lxml import html
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SEARCH_URL = "http://zefix.ch/WebServices/Zefix/Zefix.asmx/SearchFirm"

TIMEOUT = 30

REGISTRIES = {
    'ag': 'http://ag.chregister.ch',
    'ai': 'http://ai.chregister.ch',
    'ar': 'http://ar.chregister.ch',
    'be': 'http://be.chregister.ch',
    'bl': 'http://bl.chregister.ch',
    'bs': 'http://bs.powernet.ch/webservices/inet/HRG/HRG.asmx/',
    'fr': 'https://appls.fr.ch/hrcmatic/hrcintapp/',
    'ge': 'http://ge.ch/hrcintapp/',
    'gl': 'http://gl.powernet.ch/webservices/inet/HRG/HRG.asmx/',
    'gr': 'http://gr.chregister.ch',
    'ju': 'http://ju.chregister.ch',
    'lu': 'http://lu.chregister.ch',
    'ne': 'http://hrc.ne.ch/hrcintapp/',
    'nw': 'http://nw.chregister.ch',
    'ow': 'http://ow.chregister.ch',
    'sh': 'http://sh.chregister.ch',
    'sg': 'http://sg.powernet.ch/webservices/net/HRG/HRG.asmx/',
    'so': 'http://so.chregister.ch',
    'sz': 'http://sz.chregister.ch',
    'ti': 'http://ti.powernet.ch/webservices/net/HRG/HRG.asmx/',
    'tg': 'http://tg.powernet.ch/webservices/net/HRG/HRG.asmx/',
    'vd': 'https://www.rc2.vd.ch/registres/hrcintapp-pub/',
    'vs': 'http://vs.powernet.ch/webservices/net/HRG/HRG.asmx/',
    'ur': 'http://ur.chregister.ch',
    'zh': 'http://zh.powernet.ch/webservices/net/HRG/HRG.asmx/',
    'zg': 'http://zg.chregister.ch'
}


CHREGISTER_FORM = {
    "javax.faces.partial.ajax": "true",
    "javax.faces.source": "idPortalForm:auszugContentPanel",
    "primefaces.ignoreautoupdate": "true",
    "javax.faces.partial.execute": "idPortalForm:auszugContentPanel",
    "javax.faces.partial.render": "idPortalForm:auszugContentPanel",
    "idPortalForm:auszugContentPanel": "idPortalForm:auszugContentPanel",
    "idPortalForm:auszugContentPanel_load": "true",
    "idPortalForm": "idPortalForm",
    "idPortalForm:idFvFirma_hinput": "",
    "javax.faces.ViewState": "6314247452723873842:-7069064004931963664",
}

driver = webdriver.PhantomJS()


def scrape_chregister(url):
    data = {
        "persons": [],
        "companies": [],
    }

    driver.get(url)
    tree = html.fromstring(driver.page_source)
    print("hey")
    print(tree.xpath("//table[contains(@class, 'personen')]/tbody/tr"))
    wait = WebDriverWait(driver, TIMEOUT)
    # wait.until(
    #     EC.invisibility_of_element_located((By.CSS_SELECTOR, ".ui-outputpanel-loading.ui-widget"))
    # )
    # try:
    wait.until(
        EC.visibility_of_any_elements_located((By.XPATH, "//table[contains(@class, 'personen')]/tbody/tr"))
    )
    # except:
    #     print()
    #     print(driver.page_source)
    #     driver.quit()
    #     return
    print(EC.visibility_of_element_located((By.XPATH, "//table[contains(@class, 'personen')]/tbody/tr"))(driver))
    print("k")
    print(tree.xpath("//table[contains(@class, 'personen')]/tbody/tr"))
    #time.sleep(3.0)
    print("bye")
    print(tree.xpath("//table[contains(@class, 'personen')]/tbody/tr"))

    for tr in tree.xpath("//table[contains(@class, 'personen')]/tbody/tr"):
        item = {}
        attribs = tr[3].attrib
        item["cancelled"] = "class" in attribs and "strike" in attribs["class"]
        item_line = tr[3].xpath("./text()")[-1].split(",")
        if len(item_line) >= 3:
            item["last_name"] = item_line[0].strip()
            item["first_name"] = item_line[1].strip()
            data["persons"].append(item)
        else:
            item["name"] = item_line[0].strip()
            data["companies"].append(item)
    if not data["persons"]:
        return driver.page_source
    return data

SCRAPER_MAP = {
    "chregister.ch": scrape_chregister,
    #"powernet.ch": scrape_powernet,
    #"hrcintapp": scrape_hrcintapp,
}


def zefix_search(name):
    """Returns first result from a Zefix search on `name`"""
    FORM = {
        "language": "2",
        "amt": "007",
        "hrg_opt": "110000",
        "expl": "noscript",
        "page": "1",
        "id": "",
        "rf": "(pas de restriction)",
        "sitz": "(pas de restriction)",
        "sitzgem": "",
        "suche_nach": "aktuell",
        "phonetisch": "no",
    }

    FORM["name"] = name

    response = requests.post(SEARCH_URL, data=FORM)
    tree = html.fromstring(response.content)

    if "Le resultat de votre recherche est 0" in response.content:
        return None

    result = []

    # The returned HTML is broken, the <p> elements do not actually contain results,
    # as the DOM inspector would suggest.
    result["name"] = name = tree.xpath("//hr/following::b[1]/text()")[0]
    result["url"] = tree.xpath("//a[@target='_blank']/@href")[0]
    result["city"] = tree.xpath("//a[@target='_top']/text()")[0]

    return result


def scrape_company(name):
    zefix_result = zefix_search(name)

    if zefix_result is None:
        return None

    company_data = {}

    for (pattern, function) in SCRAPER_MAP.items():
        if pattern in zefix_result["url"]:
            company_data = function(zefix_result["url"])

    return company_data


    # follow link to cantonal registry

    # call parser for relevant cantonal registry

    # return data 

scrape_chregister("http://be.chregister.ch/cr-portal/auszug/auszug.xhtml?uid=CHE-110.398.897")
