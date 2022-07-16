from typing import Optional
import pydantic
import pymongo

database = pymongo.MongoClient("mongodb+srv://saifelbob2002:huhqow-mekdeg-Nizhu2@cluster0.40yph.mongodb.net/oyp?retryWrites=true&w=majority")

class UserSignUp(pydantic.BaseModel):
    name: str = Optional 
    email: str
    password: str
    isArtist: bool = Optional
    orders: list = []

class Application(pydantic.BaseModel):
    name: str
    description: str
    price: float
    images: list
    likes: int
    
class Application_From_Database(Application):
    _id: str

class Design(pydantic.BaseModel):
    title: str
    image: str
    artist: str
    link: str