# The Panama Papers Project
The aim of this project is to explore the data from the Swiss leaks and the Panama papers with a focus on Switzerland. In the first part we will construct a geographical timelapse for Switzerland showing the evolution of different activities within the country, as in this [example](https://youtu.be/310-GYiitpM). In a second part, we will examine the presence of swiss politicians and big companies in the leaked data. We will complement the data from the leaks with additional information about these entities and attempt to highlight the most relevant networks in Switzerland.

# I - Introduction: "The biggest leak in the history of data journalism"
<sup>Source: https://panamapapers.icij.org/about.html</sup>

The Panama Papers is an unprecedented investigation that reveals the offshore links of some of the globe’s most prominent figures.

The International Consortium of Investigative Journalists (ICIJ), together with the German newspaper Süddeutsche Zeitung and more than 100 other media partners, spent a year sifting through 11.5 million leaked files to expose the offshore holdings of world political leaders, links to global scandals, and details of the hidden financial dealings of fraudsters, drug traffickers, billionaires, celebrities, sports stars and more.

The trove of documents is likely the biggest leak of inside information in history. It includes nearly 40 years of data from a little-known but powerful law firm based in Panama. That firm, Mossack Fonseca, has offices in more than 35 locations around the globe, and is one of the world’s top creators of shell companies, corporate structures that can be used to hide ownership of assets.

ICIJ’s analysis of the leaked records revealed information on more than 214,000 offshore companies connected to people in more than 200 countries and territories.

The data includes emails, financial spreadsheets, passports and corporate records revealing the secret owners of bank accounts and companies in 21 offshore jurisdictions, including Nevada, Hong Kong and the British Virgin Islands.

ICIJ’s data and research unit indexed, organized and analyzed the 2.6 terabytes of data that make up the leak, using collaborative platforms to communicate and share documents with journalists working in 25 languages in nearly 80 countries.


# II - The Data

We consider the available data from the ICIJ database on the [_Panama papers_](https://offshoreleaks.icij.org/pages/database) and the _Swiss Leaks_ Github [repository](https://github.com/swissleaks/swiss_leaks_data).

The database is powered by the graph database [Neo4j](https://neo4j.com/). The graph database is a perfect fit to the type of data at hand, as it reveals the network in a natural way, applying an organization scheme similar to the human mind .The data model used by ICIJ is explained [here](https://neo4j.com/blog/analyzing-panama-papers-neo4j/). In this model, one recognizes 4 types of entities:
 
 * Clients 
 * Companies
 * Addresses
 * Officers ( which can be either a person or a company) 
 
with relationships as (using Cypher, the language used in Neo4j):

 * (:Officer)-[:is officer of]->(:Company)
  
  with the classifications:
  * protector
  * beneficiary, shareholder, director
  * beneficiary
  * shareholder
  
 * (:Officer)-[:registered address]->(:Address)
 * (:Client)-[:registered]->(:Company)
 * (:Officer)-[:has simialr name or address]->(:Address)
  
 
## Issues with the data

The ICIJ data contains a lot of duplicates, but only a small part of which is connected by a "has a similar name or address" relatioship. Another issue is that the shareholder information is stored with the "Officer", where the officer can be the share holder of any number of Companies. If the shareholder information would be stored in the "is officer of - Shareholer" relationship instead, we would remove the ambiguities in the shareholder information ([_Source_](https://neo4j.com/blog/analyzing-panama-papers-neo4j/)).
 
# III - Extending the data 
## Domain: Switzerland

There are several ways to extend and enrich the _Panama papers_ database. Unfortunately, we don't have access to big part of the data and metadata from the original leaks. On the other hand, one can look for other sources and make cross checks in order to complement the information at hand. This task is part of our project.
  
In this project, we will focus on Switzerland. Due to the public interest, it is an obvious move to cover at least two groups of entities within Switzerland:
 
 * Politicians
 * Big coorporations
 
We have pre-scanned the web for sources on the above entities. For identifying and investigating links with swiss corporations, we will make use of
 
 * [moneyhouse](https://www.moneyhouse.ch/)
     * Has well structured data on a companie's
         * Nominal capital
         * board of directors
         * managers 
         * signatories
     * More information can be purchased. We're looking for an access.
 * [opencorporates](https://opencorporates.com/)
     * The largest open database of companies in the world with 115.272.454 companies.
     * Has an open API.
 * [zefix](http://zefix.admin.ch/zfx-cgi/hrform.cgi/hraPage?alle_eintr=on&pers_sort=original&pers_num=0&language=4&col_width=366&amt=007)
      * Similar information content as money house
      * Has an API, but looks to be not well documented (and in German)
 * [wikipedia](https://en.wikipedia.org/wiki/List_of_Swiss_companies_by_revenue)
      * List of biggest swiss companies by revenue
      
 We have also access to a list of former and active swiss politicians.
          
 * https://www.parlament.ch/en/organe/national-council/members-national-council-a-z
 * https://www.parlament.ch/centers/documents/de/interessen-nr.pdf
 
 Moreover, we have a list of their _declared interests_, in which politicians officially declare which companies they support.

- https://www.parlament.ch/centers/documents/de/interessen-nr.pdf (National
  Council)
- https://www.parlament.ch/centers/documents/de/interessen-sr.pdf (Council of
  States)

The difficulty with the above information is that we have only found it in pdf
format or in the [Parliament
website](https://www.parlament.ch/en/ratsmitglieder?k=*). Both seem to be hard
to parse:
* PDF isn't easy to parse and not very reliable
* The website is mainly javascript based (with a strange access to their backend)

### Lobbying in Switzerland 
We would like to investigate these official statements about politicians declared interests and try to identify their _non-declared_ interests. We keep in mind that political campaigns in Switzerland are privately funded.
   
It is expected that these subgroups, i.e. politicians and big companies, have intersections which will naturally be highlighted. We will investigate links among people/companies based in Switzerland and those between elements outside Switzerland, whenever we consider it relevant.

One of the foreseeable achievements will be to reveal the networks in a similar fashion as it has been done in this example, for the Aliyev family in Azerbaijan: 

<img src="https://s3.amazonaws.com/dev.assets.neo4j.com/wp-content/uploads/20160408103432/azerbaijan-president-linkurious-fraud-ring.png" width=400>


# IV - Deliverables and timeplan
Several deliverables:

1. **18.11.2016**: Familiarizing with leaks data and tools (Neo4j). Start new data acquisition (Parsing the parliament's website for politician's data, MoneyHouse API access).
2. **02.12.2016**: First midterm check of the timelapse and the data acquisition/cleaning for politicians and big companies.
3. **16.12.2016**: Complementing the leaks with the acquired data and identifying the most relevant networks in Switzerland. 
4. **30.12.2016**: Finalize the timelapse and the viz for the networks.

# V - Liability
Published information has been collected carefully but no guarantee about its
completeness, correctness or up-to-date nature is given. No liability is
accepted for damage or loss incurred from any information obtained in this
repository.
