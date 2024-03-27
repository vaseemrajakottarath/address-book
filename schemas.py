from pydantic import BaseModel

class Address(BaseModel):
    id :int
    street:str
    city:str
    state:str
    latitude:float
    longitude:float

class AddressCreate(BaseModel):
    street: str
    city: str
    state:str
    latitude:float
    longitude:float