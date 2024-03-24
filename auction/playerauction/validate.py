from appdata.models import Login
from django.contrib.auth.hashers import make_password


def checkLogin(user_email,user_pass):
    user = Login.objects.get(user_email)
    response = {
        "status":"Error",
        "message":"Invalid Email or Password",
        "code":0
    }
    
    if(user):
        if user == user_pass:
            response.status = "OK"
            response.message = "Successfully logged in"
            response.code = 1  
    
    return response

def validateRegistration(data):
    return True

def storeImage():
    return "Done"

def getPassword(password):
    return make_password(password)