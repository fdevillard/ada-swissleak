# The Panama Papers Project
The aim of this project is to explore the data from the Swiss leaks and the Panama papers with a focus on Switzerland. In the first part we will construct a geographical timelapse for Switzerland showing the evolution of different activities within the country. In a second part, we will examine the presence of swiss politicians and big companies in the leaked data. We will complement the data from the leaks with additional information about these entities and attempt to highlight the most relevant networks in Switzerland.

Presentation of the project can be found here:

- [Website](https://fdevillard.github.io/ada-swissleak-website/) from presenting some results
- [Slides](https://docs.google.com/presentation/d/1N1xEphGOBkmNj8j0fFwERcmEGX81xgGT7XIZbesHHqE/edit?usp=sharing) for the presentation at the _Applied machine learning days_

# 0 - Liability
Published information has been collected carefully but no guarantee about its
completeness, correctness or up-to-date nature is given. No liability is
accepted for damage or loss incurred from any information obtained in this
repository.

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
 
# III - Augmenting the data 
There are several ways to extend and enrich the _Panama papers_ database. Unfortunately, we don't have access to big part of the data and metadata from the original leaks. On the other hand, one can look for other sources and make cross checks in order to complement the information at hand. This task is part of our project.
  
In this project, we will focus on Switzerland. Due to the public interest, it is an obvious move to cover at least two groups of entities within Switzerland:
 
 * Politicians
 * Big corporations
 
The following is an overview of different datasources that we used:
 
 * [zefix](http://zefix.admin.ch/zfx-cgi/hrform.cgi/hraPage?alle_eintr=on&pers_sort=original&pers_num=0&language=4&col_width=366&amt=007)
      * Commercial register for the legal entities in Switzerland.
      * Has an API, but bad documented at the time of writing (and in German)
      * Each results gives a link to a cantonal registry. However, Cantons are
        sharing the same plateforms (three in total). For each company, we can
        see who composes the board of the company. 
      * A parser for Zefix and the cantonal registries was written. This allows
        to obtain different information about companies such that the federal
        identification number and the composition of the board
 * [wikipedia](https://en.wikipedia.org/wiki/List_of_Swiss_companies_by_revenue)
      * List of biggest swiss companies by revenue
      * A parser for Wikipedia's table was written
 * Politicians have to give their list of interests. This is true for the
   federal parliament as well as for the cantonal ones.
      * For the federal level, data are available online using [their
        website](https://www.parlament.ch/en)
      * For the cantonal level, data are available but in different formats
        (even, sometimes, in a handwritten way...). Therefore, it's hard to
        access these data
      * The list of interests for parliamentaries at the federal level and the
        canton of Geneva have been parsed, not for the other cantons (due to
        different formats). This can be source of biaised if not used well.

Furthermore, the following are considered sources but not used at the end:
 * [moneyhouse](https://www.moneyhouse.ch/)
     * Has well structured data on a companie's
         * Nominal capital
         * board of directors
         * managers 
         * signatories
     * More information can be purchased. We're looking for an access.
     * They don't have an API for accessing their data in a convenient
       way. Thus, we tried to parse their website, without success.
 * [opencorporates](https://opencorporates.com/)
     * The largest open database of companies in the world with 115.272.454 companies.
     * Has an open API.
     * This source have some data but is very noisy. Since we're looking for
       data about Switzerland, opencorporates is too general.       

# IV - Deliverables and timeplan
Several deliverables:

1. **18.11.2016**: Familiarizing with leaks data and tools (Neo4j). Start new data acquisition (Parsing the parliament's website for politician's data, MoneyHouse API access).
2. **02.12.2016**: First midterm check of the timelapse and the data acquisition/cleaning for politicians and big companies.
3. **16.12.2016**: Complementing the leaks with the acquired data and identifying the most relevant networks in Switzerland. 
4. **30.12.2016**: Finalize the timelapse and the viz for the networks.
5. **31.01.2017**: Final deadline and presentation. Thus, creation of
presentation and a website.

# V - Delivered

## 0. An overview of Switzerland in the Panama Papers
Notebook describing differents results about the Panama Papers and the
Switzerland. Rough analysis of the CSV files from the ICIJ data and especially
the location of the different entries.

As we can see, Switzerland is well represented in the data. 

## 1. Compile parliament members and their interests
Import parliamentaries' lists of interests (federal and canton of Geneva
levels) and group the data in well formatted Dataframe.

The data is then stored in `data/all_interests.json`.

## 2. Clean interests list
Data from our data sources are dirty. This notebook is an attempt to improve the
matching between two different data sources. In this one, we focus on the
parliamentaries list of interests and Zefix lookup.

A text processing pipeline is created in order to improve the number of lookups
in Zefix.

Different functions have been moved to `helpers/language.py` in order to provide
a default pipeline for text processing or ranking the findings (tested mainly on
Zefix results).

## 3. Augment data with Zefix 
Augments the data obtained from the list of interests of the politicians with
the board members of the companies, using Zefix. 

The set-up the possibility check link of second degree between a politician and
an entry in the Panama Paper. 

## 4. Lookup politicians and their interests in the Panama Papers
This part focus on looking for politicians in the Panama papers data. Both the
politicians directly and second degree links (the ones being in the same board
as a politician) are searched. 

Some politicians are found, and several wrong positive as well (for example
people having a same same). 

## 5. More visualization
Notebook that generates other visualizations about the data like a world map,
plot per canton, and map illustrating all entities at a cantonal level.

## Other 
 * Scraping of Zefix (in `helpers/zefix_scraper.py`) allows to scrape Zefix (the
   commercial register). It offers an alternative tool than Moneyhouse (which is
   commecrial and doesn't provide any API at the moment).
 * Parsing of Wikipedia table
 * Different examples of how to use Neo4J using Jupyter notebooks

# VI - Further work
  * By centralizing all the information in a single database and scraping websites such as moneyhouse.ch or by parsing the weekly SOGC (Swiss Official Gazette of Commerce), we could have a lot more usable to data, for example to find all the companies that someone is involved in. In the case of the companies that a politician is involved in, we should in theory already have this data from their declaration of financial interests. However, as we saw in our project, this data is often incorrect, incomplete, or simply not easy to use. For example, the parliament of canton de Vaud only has declaration of interests on scanned handwritten documents.
  * It would be also useful to find a way to disambiguate entities, such as common person names or company names. This could probably be done, at least manually if we had access to the contextual documents from which the ICIJ database was built. 
