from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bson import ObjectId
from random import random, randrange
import smtplib
import pymongo
from jose import jwt
from passlib.context import CryptContext

#to check whether the password is strong or not
def isStrongPassword(password:str):
    isSpecialSymbolsIncluded = False
    for i in ["@", "!", "#", "$", "%", "^", "&", "*"]:
        if password.__contains__(i):
            isSpecialSymbolsIncluded = True

    if (password.__len__()>= 10) and (isSpecialSymbolsIncluded):
        return True

# tokenization function 
def getToken(payloads: dict):
    token = jwt.encode(claims=payloads, key="saifIsAnNuStudent202003013", algorithm="HS256")
    return token

context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#to hash the password
def hashPassword(password: str):
    return context.hash(password)

# to verify the password
def verifyPassword(password: str, hashedPassword: str) -> bool:
    return context.verify(password, hashedPassword)

#to send email to reset password 
def forgotPasswordEmail(sendTo: str):
    otp = randrange(111111, 999999)

    message = MIMEMultipart()

    message.add_header("From", "IYP")
    message.add_header("To", "you")
    message.attach(MIMEText(
    """<img src="https://i.ibb.co/9t83nkj/IYP.png" alt="IYP" border="0" />

    <body style="background-color:white">
    <br/>
    <h1>Forgot your password</h1>
    <br />
    <br />

    your OTP is:
    <h3>{}</h3>
    </body>
    """.format(otp), "html"))

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login("saifelbob2002@gmail.com", "saif@2002")
    server.sendmail("Order Your Programs", sendTo, message.as_string())
    return str(otp)

# to send verification email with OTP
def verificationEmail(sendTo: str):
    otp = randrange(111111, 999999)

    message = MIMEMultipart()


    message.add_header("From", "IYP Co.")
    message.add_header("To", "you")
    message.add_header("Subject", "Verify your OYP account")
    message.attach(MIMEText(
    """<img src="https://i.ibb.co/9t83nkj/IYP.png" alt="Iyp-black-white" border="0" width=100 />
    <body style="background-color:white">
    <br/>
    <h2>Verify your account</h2>
    your OTP is:
    <h3>{}</h3>
    </body>
    """.format(otp), "html"))

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login("saifelbob2002@gmail.com", "ryexfrtblubknrmz")
    server.sendmail("Order Your Programs", sendTo, message.as_string())
    return str(otp)

# to know if the token is for a valid user
def isValidToken(token:str) -> bool:
    database = pymongo.MongoClient("mongodb+srv://saifelbob2002:huhqow-mekdeg-Nizhu2@cluster0.40yph.mongodb.net/oyp?retryWrites=true&w=majority")
    if database['OYP']['Users'].find_one({"_id":ObjectId(jwt.decode(token, key="saifIsAnNuStudent202003013", algorithms="HS256")['data'])}):
        return True
    else:
        return False
#print(isValidToken("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiNjI3MDUxMmUyOGFiMmMxNjM5NTY0YTRiIn0.V_W6wAFeoRetl8hAJW0MLm80I-XTRcwOMuomHPT6x54"))
