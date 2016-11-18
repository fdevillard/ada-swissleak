#!/usr/bin/env python
import requests
import json

PERSON_URL = "https://ws.parlament.ch/OData.svc/Person(ID={},Language='EN')/?$format=json"
INTERESTS_URL = "https://ws.parlament.ch/OData.svc/Person(ID={},Language='EN')/PersonInterests?$format=json"

PERSON_FIELDS_TO_SAVE = (
    'DateOfBirth',
    'DateOFDeath',
    'FirstName',
    'GenderAsString',
    'LastName',
    'MilitaryRank',
    'MilitaryRankText',
    'OfficialName',
    'PlaceOfBirthCanton',
    'PlaceOfBirthCity',
    'PersonNumber'
)

INTERESTS_FIELDS_TO_SAVE = (
    'FunctionInAgencyText',
    'InterestName',
    'InterestTypeText',
    'OrganizationTypeText'
)
#TODO loops 0 to 5000 and scrape PERSON_URL
MEMBERS = []

def scrape_member(member_id):
    # Get main person info
    response = requests.get(PERSON_URL.format(member_id))

    if response.status_code != 200:
        if response.status_code == 404:
            return None
        print(response.content)
        raise RuntimeError("Received an unexpected HTTP status code {}".format(response.status_code))

    parsed_json = json.loads(response.content.decode("utf-8"))["d"]

    member_data = {field: parsed_json[field] for field in PERSON_FIELDS_TO_SAVE if field in parsed_json}

    # Get interests
    response = requests.get(INTERESTS_URL.format(member_id))
    parsed_json = json.loads(response.content.decode("utf-8"))["d"]["results"]

    member_data["Interests"] = []
    for result in parsed_json:
        interest = {field: result[field] for field in INTERESTS_FIELDS_TO_SAVE if field in result}
        member_data["Interests"].append(interest)

    return member_data

# Assume no member has an ID > 5000, which seems to be the case.
# This avoids having to parse and scrape the list page per page

for member_id in range(0, 5000):
    member = scrape_member(member_id)
    if member is not None:
        MEMBERS.append(member)

print(json.dumps(MEMBERS))
