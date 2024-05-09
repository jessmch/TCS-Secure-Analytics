from cryptography.fernet import Fernet
import time

with open("dummy_key.txt", "rb") as key_file:
    key = key_file.read()
f = Fernet(key)

# # initial encryption:
# with open("sensitive.txt", "rb") as sensitive_file:
#     token = f.encrypt(sensitive_file.read())
# with open("sensitive.bin", "wb") as encrypted_file:
#     encrypted_file.write(token)

with open("sensitive.bin", "rb") as sensitive_file:
    sensitive_info = f.decrypt(sensitive_file.read())
    print(f"processing: {sensitive_info}")
    
# simulate long-running process for memory dump
time.sleep(600)
