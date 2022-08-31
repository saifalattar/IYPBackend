from typing import Any
from pydantic import Json
import pymongo
from schemas import Design, database
from fastapi import Body ,status, APIRouter, Response
from bson import ObjectId


artist = APIRouter()

@artist.post("/iyp/{artistName}/{token}/addDesign")
def addDesign(design: Design, artistName ,token, response: Response):
    try:
        designInDatabase = database["OYP"]["designs"].insert_one(design.__dict__)
        database["OYP"][artistName+"."+token].insert_one({"designName": str(designInDatabase.inserted_id)})
        return {"success": "Design added successfully"}
    except:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"failure":"Something error happened"}

@artist.delete("/iyp/{token}/{artistName}/deleteDesign/{ID}")
def deleteDesign(token, ID, artistName):
    try:
        database["OYP"][artistName+"."+token].delete_one({"designName":ID})
        database["OYP"]["designs"].delete_one({"_id":ObjectId(ID)})
        return {"success":"Design deleted successfully"}
    except:
        return {"failure":"Design can't be deleted for now try again later"}

@artist.get("/iyp/getArtists")
def getArtists(response: Response):
    artists = []
    
    unwantedDocs = ["apps","likes","console","designs","Users"]
    for artist in database["OYP"].list_collection_names():
        name = ""
        if str(artist).startswith("IYP"):
            continue
        elif artist not in unwantedDocs:
            for letter in artist:
                if letter != ".":
                    name = name+letter
                else:
                    break
            artists.append(name)
  
    return artists

@artist.get("/iyp/{artist}/getDesigns")
def getArtistDesigns(artist, response: Response):
    allDesigns = []
    for doc in database["OYP"].list_collection_names():
        if doc.startswith(artist):
            designs = []
            for design in database["OYP"].get_collection(doc).find():
                designs.append(design['designName'])
            print(designs)
            for d in database["OYP"]["designs"].find():
                d["_id"] = str(d["_id"])
                if d["_id"] in designs:
                    allDesigns.append(d)
            return allDesigns

