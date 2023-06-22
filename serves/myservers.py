import time
from phe import paillier
import requests

class FogServer:

    def __init__(self):
        print("Fog Server : Initialise Privet Key and Public Key ...")
        self.pubkey, self.privkey = paillier.generate_paillier_keypair(n_length=512)

    def send_function(self,medicaldta,fullname,age):
        print("Crypting Your Medical Data with PHE")
      
        #Crypte data
        MedicalData = self.pubkey.encrypt(medicaldta)
 
        encrypted_data_str=str(MedicalData.ciphertext())

        medica_data_exp = str(MedicalData.exponent)
        #Send Medical Data
        print(" Fog Server : Sending Encrypted Medical Data ...")
        res = requests.post("http://localhost:3000/api/send/medicaldata/2",data=
           {
            "fullname": fullname,
            "age": age,
            "medicaldata": encrypted_data_str,
            "medicaldataExp":medica_data_exp,
            "keyN":str(self.pubkey.n)    
            }
            )
       
       #Recieve Results

    def recieve_function(self):
        print("Fog Server : Recieve Encrypted Results ... ")
 
        url = 'http://localhost:3000/api/get/results'
        response = requests.get(url)
        responseJson = response.json()
        res = responseJson
        exp =int(res['_rExpo'])
        ciphertext = int(res['_results']);
        CryptedFinalResults =  paillier.EncryptedNumber(self.pubkey, ciphertext,exp)
        print("Decrypting Results ... ")
        theFinalresults = self.privkey.decrypt(CryptedFinalResults)
        print("The Final REsults =",theFinalresults)
        return theFinalresults
    

    def getdata (self):
        print("Fog Server : Getting Your Data ...")
        url = 'http://localhost:3000/api/get/medicaldata'
        response = requests.get(url)
        responseJson = response.json()

        patient = responseJson

        print(patient)

        print(response.status_code)
        fullname = patient['_fullname']
        age =patient['_age'] 
        n = int(patient['_keyN'])
        ciphertext = int(patient['_medicaldata'])
        exp = int(patient['_medicaldataExp'])

        public_key_rec = paillier.PaillierPublicKey(n=n)
        print(public_key_rec)

        Medicaldata = paillier.EncryptedNumber(public_key_rec, ciphertext, exp)
        medicaldata = self.privkey.decrypt(Medicaldata)
        print('FULL NAME +++++',fullname)
        print("AGE +++++",age)
        print("MEDICAL DATA +++++",medicaldata)
        resulta={"fullname": fullname,
                 "age": age,
                "medicaldata": medicaldata}
        return resulta



#///////////////////////////////////////////////////////////////////////////////////////////////////////////




class MedicalStaffServer:
   

   

    def process_data(self):
        print("Application Server : Receiving Encrypted Medical Data ...")
        print("Application Server : Proccesing Your Data ...")
        
        url = 'http://localhost:3000/api/get/medicaldata'
        response = requests.get(url)
        responseJson = response.json()

        patient = responseJson


        n = int(patient['_keyN'])
        ciphertext = int(patient['_medicaldata'])
        exp = int(patient['_medicaldataExp'])

        public_key_rec = paillier.PaillierPublicKey(n=n)
        print("Regenerating public Key with n value")

        ecg = paillier.EncryptedNumber(public_key_rec, ciphertext, exp)
        #traitment
        Results = ecg + 5
     #   print("Doing Computations on Encrypted data"+Results)
       # print(str(Results.ciphertext()))
       # print(str(Results.exponent))
        print("Application Server : Sending Encrypted Results ...")
        res = requests.post("http://localhost:3000/api/send/results/2", data={
            "results": str(Results.ciphertext()),
            "rExpo": str(Results.exponent),
        })

        



