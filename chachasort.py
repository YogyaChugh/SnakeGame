from cryptography.fernet import Fernet

with open("defaults/snake.json") as f:
    data = f.read()
key = ("b'aYsD8ef0tlJpbFyFX0niY88q1NoM3Kel1IIDtikije0='"[2:-1])
key = bytes(key.encode())
print(key)
ttlbro = Fernet(key)
a = ttlbro.decrypt(data)
print(a)