from functools import partial
from geopy.geocoders import Nominatim
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


location = locator('Lagos')