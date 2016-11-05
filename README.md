# <center> The Panama Papers Project   </center>


# I - Introduction: The leaks


-- to be added

-- give appropriate credit

# II - The Data

 We consider the available data from the ICIJ database on the [_Panama papers_](https://offshoreleaks.icij.org/pages/database) and the _Swiss Leaks_ Github [repository](https://github.com/swissleaks/swiss_leaks_data). (Check if these are note the same, but in different formats. I think they are. See link in the repo).
 The database is powered by the graph database [Neo4j](https://neo4j.com/). The graph database has a perfect fit to the type of data at hand, as it reveals the network in a natural way, applying an organization scheme similar to the human mind .The data model used by ICIJ is explained [here](https://neo4j.com/blog/analyzing-panama-papers-neo4j/). In this models, one recognizes 4 types of entities:
 
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

 The ICIJ data contains a lot of duplicates, but only a small part of which is connected by a "has a similar name or address" relatioship. Another issue is that the shareholder information is stored with the 

 We devide the project into two parts. A core part, which should be more feasible and should address essencial aspects of the network reveald by the leaks. A secondary part, which might be less straightforward to achieve, it is contingent on what we find along the way.

## Links in Switzerland

In order to reveal important and potentially fraudulent relations within and with Switzerland, we will focus on three main subgroups to be identified in the data:

 -  Names associated to big coorporations
 -  Politicians
 -  The super-rich
 
 In order to do so we will make use, not restricted to, of the following sources:
 
 - https://opencorporates.com/ 
 - https://www.parlament.ch/en/organe/national-council/members-national-council-a-z
 - https://www.parlament.ch/centers/documents/de/interessen-nr.pdf
 
 
 
It is expected that these subgroups have intersections, which will naturally be highlighted. We will investigate links among people/companies based in Switzerland and those between elements outside Switzerland, whenever we consider it relevant.

The main achievent here will be to reveal the networks in a similar fashion as it has been done in this example, for the Aliyev family in Azerbaijan: 

![Aliyev Family Image](https://s3.amazonaws.com/dev.assets.neo4j.com/wp-content/uploads/20160408103432/azerbaijan-president-linkurious-fraud-ring.png)

<img src="https://s3.amazonaws.com/dev.assets.neo4j.com/wp-content/uploads/20160408103432/azerbaijan-president-linkurious-fraud-ring.png" width=400>


## Lobbying in Switzerland

Politicians in Switzerland have to declare their relations with companies. This oficial information can be obtained in

- https://www.parlament.ch/centers/documents/de/interessen-nr.pdf
- https://www.parlament.ch/centers/documents/de/interessen-sr.pdf

at national and federal levels respectively.


We would like to investigate this official statments and identify unnofical ones. We keep in mind that political campaigns in Switerland are privately funded.

