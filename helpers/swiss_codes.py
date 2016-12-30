from nltk.tokenize import RegexpTokenizer
import pandas as pd
import json

def filter_swiss(entities):
    cond_1 = entities.country_codes.str.contains('CHE')==True
    wrong_match = 'MIAMI|London|ANDORRA|Palace Yard Mews Bath|Delegate House 95 Queen|Co Kilkenny Ireland|CORPORATION TEST CLIENT|F - 74140 YVOIRE'
    cond_2 = entities.address.str.contains(wrong_match)==False
    return entities[cond_1 & cond_2]


def get_postal_codes(swiss_entities):
    tokenizer = RegexpTokenizer('(?<!\d)\d{4}(?!\d)')
    postal_codes = []
    for _,address in swiss_entities.address.iteritems():
        codes = tokenizer.tokenize(address)
        code = None
        if 'MR. ANTOINE MEKNI' in address:
            code = '1207'
        elif 'ARKION S. A. RUE DES BAINS 33' in address:
            code = '1205'
        elif 'CHEMIN DE LA JAQUE 41' in address:
            code = '1093'
        elif 'Rte De Geneva 10 Cheseax' in address:
            code = '1033'
        elif 'ZURICH' in address:
            code = '8002'
        elif 'AESCHENVORSTADT BASEL' in address:
            code = '4051'
        elif 'SOCOGESTAR S.A. SOCIETE DE CONSEILS ET DE GESTION AVENUE DE LA GRENADE' in address:
            code = '1207'
        elif 'LEXFIN ADVISORS S.A. VIA LOSANNA' in address or 'SCRIBANI & PARTNERS VIA VEGEZZI' in address:
            code = '6900'
        elif 'INCRU PROPERTIES LIMITED C/O GUILLAUME DE RHAM' in address:
            code = '1292'
        elif 'ANCA FIDUCIAIRE S.A. RUE ARNOLD-WINKELRIEDCASE' in address or \
        'CREDIT SUISSE AG OLIVIER GAILLARD – SWPZ 131; RUE DE LA MONNAIE' in address or \
        'UNITED OVERSEAS BANK P. O. BOX 2280 GENEVA' in address:
            code = '1211'
        elif 'C & H FINANCES SA ATT: MR. TULLIO COSTAS;' in address:
            code = '1260'
        elif 'MR. RICHARD G. MARRE CHALET THOMAS 1838 ROUGEMONT' in address:
            code = '1659'
        elif 'MR. OSAMA SHESHA P.O. BOX 168; ZIP 2217  MAYREN' in address:
            code = '1208'
        elif 'STONEHAGE S.A.  RUE DU PUITS-GODET 12' in address or 'Stonehage S.A. Passage Max-Meuron 1' in address:
            code = '2000'
        elif 'MR. OSCAR ORTFELDT WORLD TRADE CENTRE CP 317' in address:
            code = '6982'
        elif 'MR. HAROLD GRUENINGER HOMBURGER RECHTSANWALTE' in address:
            code = '8006'
        elif len(codes)>0:
            code = codes[-1]
        if code:
            postal_codes.append(code)
        else:
            print(address)
    return postal_codes


def get_cantons(postal_codes):
    with open('data/addresses.json', 'r') as fp:
        addresses = json.load(fp)
    cantons = []
    for pc in postal_codes:
        canton = addresses[pc]['adminCode1']
        cantons.append(canton)
    return cantons


def add_columns(swiss_entities):
    postal_codes = get_postal_codes(swiss_entities)
    cantons = pd.Series(get_cantons(postal_codes), index=swiss_entities.index)
    postal_codes = pd.Series(postal_codes, index=swiss_entities.index)
    return swiss_entities.assign(postal_code=postal_codes, canton=cantons)
