import os,sys
from cryptography.fernet import Fernet
import encryptor
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader,PdfWriter

key_set = Fernet.generate_key()

supported_extensions = [".png",".jpg",".jpeg",".ico",".icon",".json"]
disallowed = [".idea","snake_game","Snake_Game.iml","Compiling Game.run.xml","Running_Game.run.xml",".git","requirements.txt","__pycache__"]

if getattr(sys,"frozen",False):
    temp = os.path.dirname(__file__)
else:
    temp = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))

done = 0

def create_pdf(key_set):
    key_set = str(key_set)
    the_file = canvas.Canvas("Encrypted_key.pdf",pagesize=letter)
    text = the_file.beginText(50,750)
    text.setFont("Times-Roman",12)
    text.textLine(f"{key_set}")
    the_file.drawText(text)
    the_file.showPage()
    the_file.save()

def encrypt_pdf():
    read = PdfReader("Encrypted_key.pdf")
    write = PdfWriter()

    for page in read.pages:
        write.add_page(page)
    write.encrypt("snake_game_op_context_is_just_secret2133")
    with open("Encrypted_key.pdf","wb") as f:
        write.write(f)

#Recursive Function
def encrypt_files(file_or_dir):
    global done,disallowed
    done+=1
    if done>300:
        raise OverflowError("So many files to encrypt ! Might be incorrect directory set")
    print(file_or_dir)
    print(os.path.isfile(file_or_dir))
    if os.path.isfile(file_or_dir):
        print("got a file")
        filename,filename_extension = os.path.splitext(file_or_dir)
        print(filename_extension)
        if filename_extension in supported_extensions:
            print(encryptor.encrypt(os.path.abspath(file_or_dir),key_set))
        else:
            print("not a file")
            pass
    elif os.path.isdir(file_or_dir):
        print("one more dir")
        for i in os.listdir(file_or_dir):
            if i in disallowed:
                continue
            encrypt_files(os.path.join(file_or_dir,i))
    else:
        print("bruh")

print(os.listdir(temp))
for i in os.listdir(temp):
    print(i)
    if i in disallowed:
        pass
    else:
        print(os.path.join(temp,i))
        encrypt_files(os.path.join(temp,i))
create_pdf(key_set)
encrypt_pdf()