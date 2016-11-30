import time

from lxml import html, etree
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SEARCH_URL = "http://zefix.ch/WebServices/Zefix/Zefix.asmx/SearchFirm"

TIMEOUT = 30

CHREGISTER_MAX_TRIES = 10

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
}

CHREGISTER_HEADERS = {
    "Host": "be.chregister.ch",
    #"Cache-Control": "max-age=0",
    "Faces-Request": "partial/ajax",
    "Referer": "https://be.chregister.ch/cr-portal/auszug/auszug.xhtml?uid=CHE-110.398.897",
    "Accept": "application/xml, text/xml, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.8,fr;q=0.6,it;q=0.4",
    "Pragma": "no-cache",
    "Origin": "https://be.chregister.ch",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

# Dummy url to obtain another JSESSIONID
CHREGISTER_RES_URL = "https://be.chregister.ch/cr-portal/javax.faces.resource/bootstrap/css/bootstrap.min.css.xhtml;jsessionid={}?ln=default"

#driver = webdriver.PhantomJS()

def scrape_chregister(url):
    data = {
        "persons": [],
        "companies": [],
    }

    for i in range(0, CHREGISTER_MAX_TRIES):
        response = requests.get(url)
        #print(response.content)
        JS1 = response.cookies.get("JSESSIONID")

        tree = html.fromstring(response.content)

        #JS2 = requests.get(CHREGISTER_RES_URL.format(JS1)).cookies.get("JSESSIONID")

        # This kind of a CSRF token, needed to make AJAX requests
        viewstate = tree.xpath("//input[@id='j_id1:javax.faces.ViewState:0']/@value")[0]


        form_data = CHREGISTER_FORM.copy()
        form_data["javax.faces.ViewState"] = viewstate
        r = requests.post(
            "https://be.chregister.ch/cr-portal/auszug/auszug.xhtml;jsessionid={}".format(
                JS1
            ),
            data=form_data,
            headers=CHREGISTER_HEADERS,
        ).content

        if "table class" in r.decode("utf-8"):
            partial_html = etree.fromstring(r).xpath("//update[@id='idPortalForm:auszugContentPanel']/text()")[0]
            partial_tree = html.fromstring("<html>"+partial_html+"</html>")

            for tr in partial_tree.xpath("//table[contains(@class, 'personen')]/tbody/tr"):
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
            return data

    return None


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
