import geocoder 
g = geocoder.geonames('Mountain View, CA', maxRows=5)
for result in g:
  print(result.address, result.latlng)
