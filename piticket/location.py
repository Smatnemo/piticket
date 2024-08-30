from functools import partial
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
from pprint import pprint
# from piticket import project_name
states = ['Lagos','Abuja FCT', 'Kaduna']



def locator(city='',latlong=()):
    geolocator = Geolocator(user_agent='piticket')
    geocode = partial(geolocator.geocode, language='en')

    if city:
        location_details = geocode(city, language='en').raw
        return location_details['name']
    elif long_lat and isinstance(long_lat,(tuple,list)) and len(long_lat)==2:
        return geolocator.reverse(long_lat, language='en').raw['address']['state']


class Geolocator(Nominatim):
    def __init__(self,user_agent):
        Nominatim.__init__(self,user_agent=user_agent)

try:
    location = locator('Lagos')
    if location=='Laos':
        location = 'Lagos'
except GeocoderUnavailable:
    # if it cannot automatically locate itself..
    # Write code to enter it manually
    location = 'Lagos'