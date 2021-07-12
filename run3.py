from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my_user_agent")
city ="London"
country ="Uk"
loc = geolocator.geocode(city+','+ country)
print("latitude is :-" ,loc.latitude,"\nlongtitude is:-" ,loc.longitude)