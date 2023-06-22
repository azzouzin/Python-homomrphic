from fastapi import FastAPI,status
from myservers import FogServer,MedicalStaffServer
import time
from pydantic import BaseModel



app=FastAPI()

class Medical(BaseModel):
    fullname:str
    age:str
    medicaldata:int
f=FogServer()
@app.post('/server/send',status_code=status.HTTP_200_OK)
def senddata(medical:Medical):
    
    f.send_function(medical.medicaldata,medical.fullname,medical.age)

    return {'details':'success'}

@app.get('/server/recieve',status_code=status.HTTP_200_OK)
def reccieveresults():
   
    data=f.recieve_function()
    return {"results":data}

@app.get('/server/getdata',status_code=status.HTTP_200_OK)
def getdata():
 
    data=f.getdata()
    return data

@app.get('/server/process_data',status_code=status.HTTP_200_OK)
def processdata():
    m=MedicalStaffServer()
    resulta=m.process_data()

    return {'details':'success'}


##to run the project##
#1: activate the venv : pipenv shell
#2 : install the requirements : pip install -r requirements.txt
#3 :to run the project : uvicorn main:app --reload

