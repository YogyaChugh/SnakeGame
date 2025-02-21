"""This file consists of a function to encrypt/decrypt a given string/file based on a specific key.

NOTE: Any file stored on disk (snake_game) is encrypted by default"""
import os.path,warnings,random,sys
from cryptography.fernet import Fernet, InvalidToken
from PIL import Image
from PyPDF2 import PdfReader,PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

done = 0


if not getattr(sys,"frozen",False):
    paths = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    sys.path.insert(0, paths)
    temp = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
else:
    paths = ""
    temp = os.path.dirname(__file__)

key_set = Fernet.generate_key()

supported_extensions = [".png",".jpg",".jpeg",".ico",".icon",".json"]
disallowed = [".idea","snake_game","Snake_Game.iml","Compiling Game.run.xml","Running_Game.run.xml",".git","requirements.txt","__pycache__"]


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
        if os.path.splitext(location)[1] in [".ico",".icon",".png",".jpeg",".jpg"]:
            temp_image = Image.open(location)
            data = temp_image.tobytes()
        else:
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
        if os.path.splitext(location)[1] in [".ico",".icon",".png",".jpeg",".jpg"]:
            temp_image = Image.open(location)
            data = temp_image.tobytes(encoder_name="utf-8")
        else:
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


def fetch_key():
    """Used to fetch the key from the encrypted pdf"""
    reader = PdfReader("src/Encrypted_key.pdf")
    reader.decrypt("snake_game_op_context_is_just_secret2133")
    return str(reader.pages[0].extract_text())



def create_pdf(key_set):
    """Creating pdf for encryption key"""
    key_set = str(key_set)
    the_file = canvas.Canvas("Encrypted_key.pdf",pagesize=letter)
    text = the_file.beginText(50,750)
    text.setFont("Times-Roman",12)
    text.textLine(f"{key_set}")
    the_file.drawText(text)
    the_file.showPage()
    the_file.save()

def encrypt_pdf():
    """Encrypt the pdf with the same old password"""
    read = PdfReader("Encrypted_key.pdf")
    write = PdfWriter()

    #Encrypting it
    for page in read.pages:
        write.add_page(page)
    write.encrypt("snake_game_op_context_is_just_secret2133")
    with open("Encrypted_key.pdf","wb") as f:
        write.write(f)

#Recursive Function
def encrypt_files(file_or_dir):
    """Recurse through directories, encrypting allowed files"""
    global done,disallowed
    done+=1
    if done>300: #What if overflow
        done = 0
        raise OverflowError("So many files to encrypt ! Might be incorrect directory set")
    if os.path.isfile(file_or_dir): #If its a file dude
        filename,filename_extension = os.path.splitext(file_or_dir)
        if filename_extension in supported_extensions: #Only if allowed
            print(encrypt(os.path.abspath(file_or_dir),key_set))
        else:
            pass
    elif os.path.isdir(file_or_dir): #If its dir, loop through it
        for i in os.listdir(file_or_dir):
            if i in disallowed:
                continue
            encrypt_files(os.path.join(file_or_dir,i))
    else:
        pass

def start_encrypting():
    """Start encrypting files ! Only at beginning when game is installed"""
    for i in os.listdir(temp):
        print(i)
        if i in disallowed:
            pass
        else:
            encrypt_files(os.path.join(temp, i))

    global done
    done = 0
    create_pdf(key_set)
    encrypt_pdf()