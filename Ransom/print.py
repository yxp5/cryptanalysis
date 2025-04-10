#!usr/bin/env python3

# Author yxp5 >:)

import os
import time
from cryptography.fernet import Fernet

files = []
skipped = ["malware.py", "recover.py", "key.key", "print.py"]

for file in os.listdir():
	if file in skipped: continue
	else:
		fp = open(file, "r")
		print(f"Filename: {file}\tContent:\n")
		print(fp.read())
