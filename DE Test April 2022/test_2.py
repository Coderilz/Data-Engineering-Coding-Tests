# A team of analysts wish to discover how far people are travelling to their nearest
# desired court. We have provided you with a small test dataset so you can find out if
# it is possible to give the analysts the data they need to do this. The data is in
# `people.csv` and contains the following columns:
# - person_name
# - home_postcode
# - looking_for_court_type

# The courts and tribunals finder API returns a list of the 10 nearest courts to a
# given postcode. The output is an array of objects in JSON format. The API is
# accessed by including the postcode of interest in a URL. For example, accessing
# https://courttribunalfinder.service.gov.uk/search/results.json?postcode=E144PU gives
# the 10 nearest courts to the postcode E14 4PU. Visit the link to see an example of
# the output.

# Below is the first element of the JSON array from the above API call. We only want the
# following keys from the json:
# - name
# - dx_number
# - distance
# dx_number is not always returned and the "types" field can be empty.

"""
[
    {
        "name": "Central London Employment Tribunal",
        "lat": 51.5158158439741,
        "lon": -0.118745425821452,
        "number": null,
        "cci_code": null,
        "magistrate_code": null,
        "slug": "central-london-employment-tribunal",
        "types": [
            "Tribunal"
        ],
        "address": {
            "address_lines": [
                "Victory House",
                "30-34 Kingsway"
            ],
            "postcode": "WC2B 6EX",
            "town": "London",
            "type": "Visiting"
        },
        "areas_of_law": [
            {
                "name": "Employment",
                "external_link": "https%3A//www.gov.uk/courts-tribunals/employment-tribunal",
                "display_url": "<bound method AreaOfLaw.display_url of <AreaOfLaw: Employment>>",
                "external_link_desc": "Information about the Employment Tribunal"
            }
        ],
        "displayed": true,
        "hide_aols": false,
        "dx_number": "141420 Bloomsbury 7",
        "distance": 1.29
    },
    etc
]
"""

# Use this API and the data in people.csv to determine how far each person's nearest
# desired court is. Generate an output (of whatever format you feel is appropriate)
# showing, for each person:
# - name
# - type of court desired
# - home postcode
# - nearest court of the right type
# - the dx_number (if available) of the nearest court of the right type
# - the distance to the nearest court of the right type
# File start:

import csv
from rich.console import Console
import requests as req


console = Console()

def csv_to_dict(path:str) -> list[dict]:
    """Returns a list of dictionaries with the csv data"""
    with open(path) as f:
        reader = csv.DictReader(f)
        return list(reader)
    

def get_closest_court(data:list[dict], court_type:str)-> dict:
    """Given list of dicts and court type, returns the closest available court"""
    # sort courts in order of closest to home_postcode
    ordered_data = sorted(data, key=lambda x: x['distance'], reverse=False)
    for court in ordered_data:
        if court_type in court['types']:
            return court
        

def test_get_closest_court():
    """tests if the function works when 
    evaluating the closest court suitable for the persons court type works"""
    test_data = [
        {'distance':2, 'types':'test'},
        {'distance':1, 'types':'test'},
        {'distance':0, 'types':'ghghgh'}
    ]
    res = get_closest_court(test_data, 'test')
    assert res == {'distance':1, 'types':'test'}


if __name__ == "__main__":
    # [TODO]: write your answer here
    #extract people data
    data = csv_to_dict('people.csv')
    
    req_data = []

    for person in data:
        #get list of courts
        response = req.get(url=f'https://courttribunalfinder.service.gov.uk/search/results.json?postcode={person["home_postcode"]}',)
        r_json = response.json()

        #find closest court with desired type
        closest_court = get_closest_court(r_json, person['looking_for_court_type'])

        #append desired information in dictionary to a result list
        req_data.append({
            'person_name': person['person_name'],
            'court_type': person['looking_for_court_type'],
            'home_postcode': person["home_postcode"],
            'nearest_court': closest_court['name'],
            'dx_number': closest_court['dx_number'],
            'distance': closest_court['distance']
        })

    console.print(req_data)