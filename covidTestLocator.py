"""
This sample demonstrates an implementation of the Lex Code Hook Interface
in order to serve a sample bot which manages reservations for hotel rooms and car rentals.
Bot, Intent, and Slot models which are compatible with this sample can be found in the Lex Console
as part of the 'BookTrip' template.

For instructions on how to set up and test this bot, as well as additional samples,
visit the Lex Getting Started documentation http://docs.aws.amazon.com/lex/latest/dg/getting-started.html.
"""

import datetime
import time
import os
import dateutil.parser
import logging
import json
import urllib3
from math import cos, asin, sqrt
from uszipcode import SearchEngine

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# --- Helpers that build all of the responses ---


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


# --- Helper Functions ---


def safe_int(n):
    """
    Safely convert n value to int.
    """
    if n is not None:
        return int(n)
    return n


def try_ex(func):
    """
    Call passed in function in try block. If KeyError is encountered return None.
    This function is intended to be used to safely access dictionary.

    Note that this function would have negative impact on performance.
    """

    try:
        return func()
    except KeyError:
        return None



def build_validation_result(isvalid, violated_slot, message_content):
    return {
        'isValid': isvalid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


# --- Intents ---


# This is crazy: https://stackoverflow.com/questions/41336756/find-the-closest-latitude-and-longitude
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


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'GetLocation':
        return get_location(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


# --- Main handler ---


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)