from cryptography.fernet import Fernet

class Asydecryption:   

    def __init__(self):
        self.decfile = ""             

    def decryption(self,fcontent,skey): 
        #public_key = Fernet.generate_key()

        signature_gen = Fernet(skey)

        self.decfile = signature_gen.decrypt(fcontent) 

        return self.decfile.decode()
        
