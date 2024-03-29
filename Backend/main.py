import json
from fastapi import Body, FastAPI ,status, APIRouter, Response
from pydantic import Json
import pymongo
from functions import getToken, hashPassword, isStrongPassword, isValidToken
from schemas import database
from admin import adminRouter
from auth import authRouter
from designer import artist


app = FastAPI()

@app.get("/")
def hello():
    return "Hello"

# to get all apps from specific category
@app.get("/oyp/allApps/{document}/{token}")
def getAllApps(token, document, response:Response):
    apps = []
    if isValidToken(token):
        for app in database["OYP"][document].find():
            app['_id'] = str(app["_id"]) 
            apps.append(app)
        return apps
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"failure": "not authorized to view this content"}

# to get specific app 
@app.get('/oyp/{token}/{appId}')
def goToApp(token, appId, response:Response):
    if isValidToken(token):
        for app in database['OYP']['apps'].find():
            if appId == str(app["_id"]):
                app["_id"] = str(app["_id"])
                return app
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"failure": "Can't access this content"}
    
    
    
@app.put("/oyp/{category}/{appId}")
def likeApp(category, appId,response: Response, nLikes : dict = Body(...) ):
    if nLikes["add"]:
        try:
            database["OYP"]["likes"].insert_one({"id":appId})
            return True
        except:
            response.status_code = status.HTTP_404_NOT_FOUND
            return False
    else:
        try:
            database["OYP"]["likes"].delete_one({"id":appId})
            return True
        except :
            response.status_code = status.HTTP_404_NOT_FOUND
            return False

@app.get("/oyp/likes/{appId}/isliked")
def isliked(appId):
    if(database["OYP"]["likes"].find_one({"id":appId}) == None):
        return False
    else:
        return True




app.include_router(authRouter)
app.include_router(adminRouter)
app.include_router(artist)
