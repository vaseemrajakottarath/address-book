from fastapi import FastAPI, HTTPException, Depends,Query
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func

from geopy.geocoders import Nominatim

import  schemas
from database import SessionLocal, engine,AddressDB

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

geolocator = Nominatim(user_agent="address_lookup1ee")

@app.post("/addresses/", response_model=schemas.AddressCreate)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    # Perform coordinate lookup based on street, city, and state
    full_address = f"{address.street}, {address.city}, {address.state}"
    location = geolocator.geocode(full_address)
    if location is None:
        raise HTTPException(status_code=400, detail="Could not find coordinates for the address")

    # Extract latitude and longitude from the location
    latitude = location.latitude
    longitude = location.longitude

    # Create the AddressDB object with the provided data and coordinates
    db_address = AddressDB(
       
        street=address.street,
        city=address.city,
        state=address.state,
        latitude=latitude,
        longitude=longitude
    )

    # Add the address to the database and commit the transaction
    db.add(db_address)
    db.commit()
    db.refresh(db_address)

    # Return the newly created address
    return db_address

#Retrieve all addresses including id details
@app.get("/all_addresses/", response_model=List[schemas.Address])
def get_addresses(db: Session = Depends(get_db)):
    return db.query(AddressDB).all()

#Retrieve details of a specific address
@app.get("/addresses/{address_id}", response_model=schemas.Address)
def get_address(address_id: int, db: Session = Depends(get_db)):
    db_address = db.query(AddressDB).filter(AddressDB.id == address_id).first()
    if db_address:
        return db_address
    else:
        raise HTTPException(status_code=400, detail="Invalid address id")

#Retrieve address based on lat,long and within distance
@app.get("/addresses/nearby/", response_model=List[schemas.Address])
def get_addresses_nearby(
    lat: float = Query(..., description="Latitude of the location"),
    lon: float = Query(..., description="Longitude of the location"),
    distance: float = Query(..., description="Maximum distance in kilometers"),
    db: Session = Depends(get_db)
):
    # Perform spatial query to fetch nearby addresses
    nearby_addresses = (
        db.query(AddressDB)
        .filter(
            func.sqrt(
                func.pow(AddressDB.latitude - lat, 2) +
                func.pow(AddressDB.longitude - lon, 2)
            ) <= distance / 111.12  # Convert distance from kilometers to degrees (approximately 111.12 km per degree of latitude)
        )
        .all()
    )
    return nearby_addresses

#Update street,city and state
@app.put("/addresses/{address_id}",response_model = schemas.AddressCreate)
def update_address(address_id :int,address_data:schemas.AddressCreate,db: Session =Depends(get_db)):

    db_address =db.query(AddressDB).filter(AddressDB.id == address_id).first()

    if not db_address:
        raise HTTPException(status_code=404,detail ="Address not found")
    
    db_address.street = address_data.street
    db_address.city = address_data.city
    db_address.state = address_data.state

    full_address = f"{address_data.street}, {address_data.city}, {address_data.state}"
    location = geolocator.geocode(full_address)
    if location is None:
        raise HTTPException(status_code=400, detail="Could not find coordinates for the address")

    db_address.latitude = location.latitude
    db_address.longitude = location.longitude

    db.commit()
    db.refresh(db_address)
    return db_address

#delete address by id
@app.delete("/delete_address/{address_id}")
def delete_address(address_id :int ,db:Session=Depends(get_db)):

    db_address= db.query(AddressDB).filter(AddressDB.id == address_id).first()
    if  db_address:
        db.delete(db_address)
        db.commit()
        return {"message":f"Address_id:{address_id} deleted successfully"}   
    else:
        raise HTTPException(status_code=404, detail="Address not found")
    