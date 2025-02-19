"""This file consists of a function to encrypt/decrypt a given string/file based on a specific key.

NOTE: Any file stored on disk (snake_game) is encrypted by default"""
from sys import exception
import os.path,warnings
from cryptography.fernet import Fernet

def encrypt(location):
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

    #Main Logic
    key = Fernet.generate_key()
    temp = Fernet(key)
    token = temp.encrypt(data.encode())
    return (key,token)

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
    temp_dude = Fernet(key)
    print(temp_dude)
    data_work = temp_dude.decrypt(data).decode()
    return data_work


if __name__ == "__main__":
    #Trial code ! Remove later
    a = encrypt("C:\\Users\\Lenovo\\OneDrive\\Desktop\\Snake_Game\\src\\Snake\\saved_snakes.json")
    print(a)
    with open("C:\\Users\\Lenovo\\OneDrive\\Desktop\\Snake_Game\\src\\Snake\\saved_snakes.json",'w') as file:
        file.write(a[1].decode())
    b = decrypt("C:\\Users\\Lenovo\\OneDrive\\Desktop\\Snake_Game\\src\\Snake\\saved_snakes.json",a[0])
    print(b)

