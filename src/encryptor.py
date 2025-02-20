"""This file consists of a function to encrypt/decrypt a given string/file based on a specific key.

NOTE: Any file stored on disk (snake_game) is encrypted by default"""
import os.path,warnings,random
from cryptography.fernet import Fernet, InvalidToken


class EncryptionError(Exception):
    def __init__(self,message):
        self.message = message
        super().__init__(self.message)

def encrypt(location,key):
    """Encrypts a particular file/string and returns the key which can be used to retrieve the data!"""

    #Input checking
    if not isinstance(location,str):
        raise ValueError("Please pass a string to the file location! Type passed: ",type(location))
    if os.path.isfile(location):
        with open(location, "r",encoding="utf-8") as file:
            data = file.read()
    else:
        warnings.warn("String supplied isn't a file ! Further processing it as the encryption/decryption string")
        data = location

    #Main Logic (Just Yogya knows)
    #Works with double encryption
    temp = Fernet(key)
    try:
        if not isinstance(data,bytes):
            token = temp.encrypt(data.encode()) #Generate token - 1st encryption
        else:
            token = temp.encrypt(data)
    except TypeError as e:
        raise EncryptionError("File Encryption failed !")
    except InvalidToken as d:
        raise EncryptionError("File Encryption failed !")
    gg_token = str(token) #String Token
    gg_token = gg_token[2:-1] #Remove b" and " from beg and end
    new_temp_key = str(key) #Byte key to string
    new_temp_token = "" #To store the double encrypted token
    j = 0
    mega = random.randint(1,6) #Genrating special int to modify token
    new_temp_token += "e" #To tell file is encrypted
    new_temp_token += str(mega) #Add the special int
    for i in range(len(gg_token)):
        if i%mega == 0 and not j==len(new_temp_key): #Adds key to the token
            new_temp_token += (new_temp_key[j] + gg_token[i])
            j+=1
        else:
            new_temp_token += gg_token[i]
    if j!=len(new_temp_key): #Adds key at end if key not distributed inside the token fully
        new_temp_token +=new_temp_key[j:]
    return bytes(new_temp_token.encode())

def decrypt(location,key):
    """Decrypts a particular file/string and returns the decrypted data!"""

    #Input checking
    if not isinstance(location,str):
        raise ValueError("Please pass a string to the file location! Type passed: ",type(location))
    if not isinstance(key,bytes):
        raise ValueError("Please pass bytes to the file location! Type passed: ",type(key))
    if os.path.isfile(location):
        with open(location, "r",encoding="utf-8") as file:
            data = file.read()
    else:
        warnings.warn("String supplied isn't a file ! Further processing it as the encryption/decryption string")
        data = location

    #Main Logic
    temp_usage = Fernet(key)
    data = str(data)    #Just in case
    #If user sent without converting to string
    if data[0]=="b" and ((data[1]== "\"" and data[-1]=="\"") or (data[1]== "'" and data[-1]=="'")):
        data = data[2:-1]

    #If file already encrypted
    if data[0]!="e":
        raise ValueError("File is already decrypted !")
    mega = int(data[1]) #the special int
    new_data = ""   #to store the real token
    temp_var = (len(data)-2 - len(key)) + int((len(data)-2 - len(key))/mega) #Getting the length of the token with keys inserted in between
    #above one, subtracts from length the key if at end as well as e and special key at beginning
    data = str(data[2:(temp_var+2)])    #Get the new data
    for i in range(len(data)):  #Add real data to new_data
        if i%(mega+1)!=0:
            new_data += data[i]
    new_data.encode()
    try:
        data_work = temp_usage.decrypt(new_data).decode() #Decrypt
    except TypeError as e:
        raise EncryptionError("File Decryption failed !")
    except InvalidToken as d:
        raise EncryptionError("File Decryption failed !")
    #TWO LAYER PROTECTION :)
    return data_work