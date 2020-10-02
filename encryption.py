from cryptography.fernet import Fernet

# Run this to generate key file
def genwrite_key():
    key = Fernet.generate_key()
    with open("pass.key", "wb") as key_file:
        key_file.write(key)

def call_key():
    return open("pass.key", "rb").read()

key = call_key()
f = Fernet(key)
def encrypt_string(_string):
    return f.encrypt(_string.encode()).decode()

def decrypt_string(_string):
    return f.decrypt(_string.encode()).decode()