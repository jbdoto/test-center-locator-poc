import json
import urllib3
from math import cos, asin, sqrt
from uszipcode import SearchEngine
import pprint


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))

def closest(data, v):
    return min(data, key=lambda p: distance(v['lat'],v['lon'], float(p['lat']),float(p['lon'])))

def get_location(intent_request):

    zipcode = intent_request['zipcode']
    search = SearchEngine(simple_zipcode=True) # set simple_zipcode=False to use rich info database
    zipcode = search.by_zipcode(zipcode)
    #print(zipcode)
    zipcode_dict = zipcode.to_dict()
    state = zipcode_dict['state']

    #print('getting closest location for state={}'.format(state))

    api = "https://sheetlabs.com/NCOR/covidtestcentersinUS?state={}".format(state)
    http = urllib3.PoolManager()
    response = http.request('GET', api)
    test_locations = json.loads(response.data.decode('utf-8'))
    #pprint.pprint(test_locations)
    # look up person's ZIP code...get state, then query above API.
    # find closest center by lat/lon:
    # https://pypi.org/project/pgeocode/
    #
    # {
    #     lastupdateddate: "3/17/2020",
    #     centername: "Penn Medicine Radnor",
    #     address: "250 King of Prussia Rd, Radnor, PA 19087",
    #     city: "Randor",
    #     state: "PA",
    #     lat: "40.0426806",
    #     lon: -75.3582008,
    #     url: "https://www.phillyvoice.com/coronavirus-testing-drive-thru-philadelphia-penn-medicine-covid-19/",
    #     telephone: null,
    #     moreinfo: null,
    #     drivethru: "O"
    # }
    #current_lat_lon = {'lat': 39.7622290, 'lon': -86.1519750}
    #print(zipcode_dict)
    current_lat_lon = {'lat': zipcode_dict['lat'], 'lon': zipcode_dict['lng']}
    closest_location = closest(test_locations, current_lat_lon)
    pprint.pprint(closest_location)
    return closest_location

get_location({'zipcode': '19072'})
print("-----------------------------------\n")
# get_location({'state': 'PA'})
# print("-----------------------------------\n")
# get_location({'state': 'NJ'})
# print("-----------------------------------\n")
# get_location({'state': 'DE'})
# print("-----------------------------------\n")
# get_location({'state': 'NY'})
#
