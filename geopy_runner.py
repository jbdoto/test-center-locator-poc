from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="test_app")
location = geolocator.geocode("19072")
print(location)
