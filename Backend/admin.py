from Backend.functions import forgotPasswordEmail, getToken, hashPassword, isStrongPassword, verificationEmail, verifyPassword
from Backend.schemas import Application, Design, UserSignUp, database
from fastapi import APIRouter, Body, status, Response
import pymongo

adminRouter = APIRouter()

# to add a new app by the admin
@adminRouter.post("/OYP/admin/saif/addnewapp/{document}")
def addNewApp(document ,newApp: Application, response:Response):
    try:
        database['OYP'][document].insert_one(newApp.__dict__)
        return {"success":"App added successfully"}
    except:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"failure":"There is something error"}

@adminRouter.post("/OYP/admin/addnewdesign")
def addNewDesign(design: Design ,response: Response):
    try:
        database["OYP"]["designs"].insert_one(design.__dict__)
        return {"success":"Your design uploaded succefully"}
    except:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {"failure":"There is something error try again later"} 