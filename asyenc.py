from cryptography.fernet import Fernet

class Asyencryption:   

    def __init__(self):
        self.encfile = ""  
        self.pukey = ""    

    def encryption(self,fcontent): 

        public_key = Fernet.generate_key()
        signature_gen = Fernet(public_key)

        self.encfile = signature_gen.encrypt(fcontent)
        self.pukey = public_key
        return self.encfile.decode(), self.pukey.decode()
        
