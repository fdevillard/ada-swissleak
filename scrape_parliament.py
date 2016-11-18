#!/usr/bin/env python
"""
Parses data from parlament.ch to parliament_members_interests.json.

It shouldn't be run again unless the json file is lost."""

import datetime
import json
import requests


PERSON_URL = "https://ws.parlament.ch/OData.svc/Person(ID={},Language='EN')/?$format=json"
INTERESTS_URL = "https://ws.parlament.ch/OData.svc/Person(ID={},Language='EN')/PersonInterests?$format=json"
COUNCIL_HISTORIES_URL = "https://ws.parlament.ch/OData.svc/MemberCouncil(ID={},Language='EN')/MemberCouncilHistories?$format=json"

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

#TODO limit year to swissleaks years

def read_date(value):
    return datetime.datetime.fromtimestamp(float(value[6:-2])/1000)

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

    # Get dates of activity

    member_data["Active"] = False
    join_dates = []
    leave_dates = []

    response = requests.get(COUNCIL_HISTORIES_URL.format(member_id))
    parsed_json = json.loads(response.content.decode("utf-8"))["d"]["results"]

    for result in parsed_json:
        join_dates.append(read_date(result["DateJoining"]))
        if result["Active"]:
            member_data["Active"] = True
        else:
            leave_dates.append(read_date(result["DateLeaving"]))

    member_data["DateJoining"] = min(join_dates)

    if not member_data["Active"]:
        member_data["DateLeaving"] = max(leave_dates)
    else:
        member_data["DateLeaving"] = None

    return member_data

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

# Assume no member has an ID > 5000, which seems to be the case.
# This avoids having to parse and scrape the list page per page

for member_id in range(4102, 4103):
    member = scrape_member(member_id)
    if member is not None:
        MEMBERS.append(member)

print(json.dumps(MEMBERS, default=json_serial))
