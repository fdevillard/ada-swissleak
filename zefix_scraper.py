from random import random
import time

from lxml import html

SEARCH_URL = "https://www.moneyhouse.ch/fr/search?q={}&status=1&tab=companies"


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



def scrape_company(name):
    # Search for name

    # return None if no results

    # or pick first result

    # follow link to cantonal registry

    # call parser for relevant cantonal registry

    # return data 