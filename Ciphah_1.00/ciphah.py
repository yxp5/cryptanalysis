# Author: yxp5

import tkinter as tk
import tkinter.ttk as ttk
import math
import binascii
import struct
import time

# Definitions
root = tk.Tk()
root.title("Ciphah!")
PI = math.pi - 3

prompt = ""
txt_display = ""
complexity = 1
cnt = 0
bias_stack = []

# Used in enc4 algorithm (SHA-512)
initial_hash = (
    0x6a09e667f3bcc908,
    0xbb67ae8584caa73b,
    0x3c6ef372fe94f82b,
    0xa54ff53a5f1d36f1,
    0x510e527fade682d1,
    0x9b05688c2b3e6c1f,
    0x1f83d9abfb41bd6b,
    0x5be0cd19137e2179,
)

round_constants = (
    0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f,
    0xe9b5dba58189dbbc, 0x3956c25bf348b538, 0x59f111f1b605d019,
    0x923f82a4af194f9b, 0xab1c5ed5da6d8118, 0xd807aa98a3030242,
    0x12835b0145706fbe, 0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
    0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235,
    0xc19bf174cf692694, 0xe49b69c19ef14ad2, 0xefbe4786384f25e3,
    0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65, 0x2de92c6f592b0275,
    0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
    0x983e5152ee66dfab, 0xa831c66d2db43210, 0xb00327c898fb213f,
    0xbf597fc7beef0ee4, 0xc6e00bf33da88fc2, 0xd5a79147930aa725,
    0x06ca6351e003826f, 0x142929670a0e6e70, 0x27b70a8546d22ffc,
    0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
    0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6,
    0x92722c851482353b, 0xa2bfe8a14cf10364, 0xa81a664bbc423001,
    0xc24b8b70d0f89791, 0xc76c51a30654be30, 0xd192e819d6ef5218,
    0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8,
    0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 0x2748774cdf8eeb99,
    0x34b0bcb5e19b48a8, 0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb,
    0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3, 0x748f82ee5defb2fc,
    0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
    0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915,
    0xc67178f2e372532b, 0xca273eceea26619c, 0xd186b8c721c0c207,
    0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178, 0x06f067aa72176fba,
    0x0a637dc5a2c898a6, 0x113f9804bef90dae, 0x1b710b35131c471b,
    0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc,
    0x431d67c49c100d4c, 0x4cc5d4becb3e42b6, 0x597f299cfc657e2a,
    0x5fcb6fab3ad6faec, 0x6c44198c4a475817,
)

# Commands
def displayUpdate():
    global screen, txt_display, cnt
    screen.config(state="normal")
    screen.delete("1.0", tk.END)
    screen.insert(tk.END, f"{txt_display} ({cnt})")
    screen.config(state="disable")

def resetGV():
    global cnt, bias_stack
    cnt = 0
    bias_stack = []

def enter():
    global prompt, txt_display, cnt
    prompt = entry1.get()
    if len(prompt) > 200:
        txt_display = "Error! Input must not exceed 200 characters."
    else:
        txt_display = prompt
    resetGV()
    displayUpdate()

def cmpx1():
    global complexity
    complexity = 1
    config()
    enter()

def cmpx2():
    global complexity
    complexity = 2
    config()
    enter()

def cmpx3():
    global complexity
    complexity = 3
    config()
    enter()

def cmpx4():
    global complexity
    complexity = 4
    config()
    enter()

def enc1():
    global cnt, txt_display
    if txt_display == "": return
    
    enc = ""
    for index, char in enumerate(txt_display):
        enc += chr((ord(char) - 32 + index - 3) % 95 + 32)
    cnt += 1
    txt_display = enc
    buttonConfig()
    displayUpdate()

def dec1():
    global cnt, txt_display
    if cnt == 0: return
    
    dec = ""
    for index, char in enumerate(txt_display):
        dec += chr((ord(char) - 32 - index + 3) % 95 + 32)
    cnt -= 1
    txt_display = dec
    buttonConfig()
    displayUpdate()

def enc2():
    global cnt, txt_display, bias_stack
    if txt_display == "": return
    
    enc = ""
    bias = 0
    for index, char in enumerate(txt_display):
        bias += (ord(char) + 3) // ((index % 9) + 3)
    bias_stack.append(bias)
    for index, char in enumerate(txt_display):
        enc += chr((ord(char) - 32 +
                    int(round(((index+1%10)+PI)*(math.pi**2), 10)*pow(10, 10)) +
                    int(round(bias*PI*(index+1), 10))*pow(10, 10)) % 95 + 32)
    cnt += 1
    txt_display = enc
    buttonConfig()
    displayUpdate()

def dec2():
    global cnt, txt_display, bias_stack
    if cnt == 0: return
    
    dec = ""
    bias = bias_stack.pop()
    for index, char in enumerate(txt_display):
        dec += chr((ord(char) - 32 -
                    int(round(((index+1%10)+PI)*(math.pi**2), 10)*pow(10, 10)) -
                    int(round(bias*PI*(index+1), 10))*pow(10, 10)) % 95 + 32)
    cnt -= 1
    txt_display = dec
    buttonConfig()
    displayUpdate()

def enc3():
    global cnt, txt_display, bias_stack
    if txt_display == "": return
    if cnt == 1 and complexity != 4: return
    size = bin(len(txt_display))[2:]
    if len(size) < 8: size = '0'*(8-len(size)) + size
    padding = 'a' * (256 - 8 - len(txt_display))
    txt_formatted = txt_display.replace('a', '\x1f') + padding + size
    
    enc = ""
    bias = 0
    for index, char in enumerate(txt_formatted):
        bias += (ord(char) + 3) // ((index % 9) + 3)
    bias_stack.append(bias)
    for index, char in enumerate(txt_formatted):
        enc += chr((ord(char) - 32 + 
                    int(round(((index+1%10)+PI)*(math.pi**2), 10)*pow(10, 10)) +
                    int(round(bias*PI*(index+1), 10))*pow(10, 10)) % 95 + 32)
    cnt += 1
    txt_display = enc
    buttonConfig()
    displayUpdate()

def dec3():
    global cnt, txt_display, bias_stack
    if cnt == 0: return
    
    dec = ""
    bias = bias_stack.pop()
    for index, char in enumerate(txt_display):
        dec += chr((ord(char) - 32 - 
                    int(round(((index+1%10)+PI)*(math.pi**2), 10)*pow(10, 10)) -
                    int(round(bias*PI*(index+1), 10))*pow(10, 10)) % 95 + 32)
    cnt -= 1
    txt_formatted = dec.replace('\x1f', 'a')
    
    size = int(txt_formatted[248:], 2)
    txt_display = txt_formatted[:size]
    buttonConfig()
    displayUpdate()

def rightRotate(n, bits):
    return (n >> bits) | (n << (64 - bits)) & 0xFFFFFFFFFFFFFFFF

def sha512(message):
    # Credit to Illia Volochii
    if type(message) is not str:
        raise TypeError('Given message should be a string.')
    message_array = bytearray(message, encoding='utf-8')

    mdi = len(message_array) % 128
    padding_len = 119 - mdi if mdi < 112 else 247 - mdi
    ending = struct.pack('!Q', len(message_array) << 3)
    message_array.append(0x80)
    message_array.extend([0] * padding_len)
    message_array.extend(bytearray(ending))

    sha512_hash = list(initial_hash)
    for chunk_start in range(0, len(message_array), 128):
        chunk = message_array[chunk_start:chunk_start + 128]

        w = [0] * 80
        w[0:16] = struct.unpack('!16Q', chunk)

        for i in range(16, 80):
            s0 = (
                rightRotate(w[i - 15], 1) ^
                rightRotate(w[i - 15], 8) ^
                (w[i - 15] >> 7)
            )
            s1 = (
                rightRotate(w[i - 2], 19) ^
                rightRotate(w[i - 2], 61) ^
                (w[i - 2] >> 6)
            )
            w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & 0xFFFFFFFFFFFFFFFF

        a, b, c, d, e, f, g, h = sha512_hash

        for i in range(80):
            sum1 = (
                rightRotate(e, 14) ^
                rightRotate(e, 18) ^
                rightRotate(e, 41)
            )
            ch = (e & f) ^ (~e & g)
            temp1 = h + sum1 + ch + round_constants[i] + w[i]
            sum0 = (
                rightRotate(a, 28) ^
                rightRotate(a, 34) ^
                rightRotate(a, 39)
            )
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = sum0 + maj

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFFFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFFFFFFFFFF

        sha512_hash = [
            (x + y) & 0xFFFFFFFFFFFFFFFF
            for x, y in zip(sha512_hash, (a, b, c, d, e, f, g, h))
        ]

    return binascii.hexlify(
        b''.join(struct.pack('!Q', element) for element in sha512_hash),
    ).decode('utf-8')

def enc4():
    # SHA-512
    global cnt, txt_display
    if txt_display == "": return
    
    enc = sha512(txt_display)
    txt_display = enc
    enc3()
    
    buttonConfig()
    displayUpdate()

def dec4():
    print("Invalid operation, SHA-512 is not designed to be decrypted!")

def buttonConfig():
    btn_info.config(text=f"Current complexity: Level {complexity}")

def config():
    if complexity == 1:
        btn_enc.config(command=enc1)
        btn_dec.config(command=dec1)
    elif complexity == 2:
        btn_enc.config(command=enc2)
        btn_dec.config(command=dec2)
    elif complexity == 3:
        btn_enc.config(command=enc3)
        btn_dec.config(command=dec3)
    elif complexity == 4:
        btn_enc.config(command=enc4)
        btn_dec.config(command=dec4)
    buttonConfig()

def toggleInfo():
    global txt_display
    resetGV()
    txt_display = "CMPX stands for complexity level of the encryption scheme, and it defines how " \
                  "hard it is to break the encryption using attacks. Level 1 uses the Caesar " \
                  "Cipher, which only applies a shift to all characters. Level 2 adds the Avalanche " \
                  "Effect, which output a better pseudorandom-looking encryption. Level 3 only runs " \
                  "for once and limits the maximum input length, but features constant output length. " \
                  "Level 4 is an implementation of SHA-512 algorithm, which includes round function."
    displayUpdate()

frame = ttk.Frame(root, padding=10)
frame.grid()

# Prompt
entry1 = tk.Entry(frame, width=50, bg="gray")
entry1.grid(column=0, row=0, columnspan=3, sticky="W", pady=5, ipadx=2, ipady=2)
ttk.Button(frame, text="Enter", command=enter).grid(column=3, row=0, sticky="E")

# Selected files
screen = tk.Text(frame, state="disable", bg="gray")
screen.grid(column=0, row=1, columnspan=4, sticky="EW", pady=10)

# Options
buttons_frame = ttk.Frame(frame)
buttons_frame.grid(column=0, row=2, sticky="W")
btn_info = ttk.Button(buttons_frame, text=f"Current complexity: Level {complexity}", command=None, state="disable")
btn_info.grid(column=0, row=2, sticky="W")
btn_enc = ttk.Button(buttons_frame, text="ENCRYPT", command=None)
btn_enc.grid(column=1, row=2, sticky="W")
btn_dec = ttk.Button(buttons_frame, text="DECRYPT", command=None)
btn_dec.grid(column=2, row=2, sticky="W")

menu = tk.Menu(root)
cmpx = tk.Menu(menu)
cmpx.add_command(label='Level 1 CMPX', command=cmpx1)
cmpx.add_command(label='Level 2 CMPX', command=cmpx2)
cmpx.add_command(label='Level 3 CMPX', command=cmpx3)
cmpx.add_command(label='Level 4 CMPX', command=cmpx4)
menu.add_cascade(label='Select CMPX', menu=cmpx)
info = tk.Menu(menu)
info.add_command(label='Info', command=toggleInfo)
menu.add_cascade(label='Help', menu=info)
root.config(menu=menu)

config()

ttk.Button(frame, text="Close", command=root.destroy).grid(column=3, row=2, sticky="E")
root.mainloop()









