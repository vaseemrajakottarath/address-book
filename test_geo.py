from geopy.geocoders import Nominatim
from fastapi import FastAPI, HTTPException, Depends,Query


geolocator = Nominatim(user_agent="address_lookup1ee")

street ="church street"
city ="Bengaluru"
state ="karnataka"


full_address = f"{street}, {city}, {state}"
location = geolocator.geocode(full_address)
if location is None:
    raise HTTPException(status_code=400, detail="Could not find coordinates for the address")

print("latitude",location.latitude)
print("longitude",location.longitude)