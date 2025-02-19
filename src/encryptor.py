"""This file consists of a function to encrypt/decrypt a given string/file based on a specific key.

NOTE: Any file stored on disk (snake_game) is encrypted by default"""
from sys import exception
import os.path,warnings

def encrypt_decrypt(location,special_key,e_d="e"):
    """Encrypts/decrypts a particular file/string and returns the string containing its content
    based on the secret key passed as the second argument! Note 3rd argument to be either 'e' or 'd'
    NOTE: Max length of secret_key to be 5"""

    #Input checking
    if not isinstance(location,str):
        raise ValueError("Please pass a string to the file location! Type passed: ",type(location))
    if len(str(special_key))>5:
        raise ValueError("Special key can't be more than 5 digits ! Current length: ",len(special_key))
    if not isinstance(special_key,int):
        raise ValueError("Special key passed is of wrong type ! Current type: ",type(str))
    if e_d != "e" and e_d != "d":
        raise ValueError("Unintended value passed for encrypt/decrypt ! e_d value: ",e_d)
    if os.path.isfile(location):
        with open(location, "r") as file:
            data = file.read()
    else:
        warnings.warn("String supplied isn't a file ! Further processing it as the encryption/decryption string")
        data = location

    #Main Logic
    new=""
    for i in range(len(data)):
        temp = ord(data[i])
        if e_d=="e":
            temp+=special_key
        elif e_d=="d":
            temp-=special_key
        new += chr(temp)
    return new

if __name__ == "__main__":
    #Trial code ! Remove later
    a = encrypt_decrypt("C:\\Users\\Lenovo\\OneDrive\\Desktop\\Snake_Game\\src\\Maps\\saved_maps.json",33433)
    print(a)
    print(encrypt_decrypt(a,33433,'d'))

