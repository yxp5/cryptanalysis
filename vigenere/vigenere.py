# Author: yxp5
import math
import string
import freqAnalysis as fa
import random

# =================================
# Cryptanalysis of Vigenere
# =================================
def ngramMaxFrequency(n, text, PRINT=False):
    """
    int -> str -> bool -> list(str)
    
    Input: length of gram (n), text to be analyzed (text)
    Output: a list of ngrams in text that has maximum frequency
    
    Print: result information
    """
    frequency = {}
    length = len(text)
    for i in range(length - n):
        frequency.update({text[i:i+n]: frequency.get(text[i:i+n], 0) + 1})

    # Find trigram with largest frequency
    max_val = max(frequency.values())
    res = list(filter(lambda x: frequency[x] == max_val, frequency))

    if PRINT: 
        print("Maximum frequency for " + str(n) + "grams: ", max_val)
        print("Keys with maximum values are: " + str(res))
    
    return res

def distanceBetweenSubtext(subtext, text : str, PRINT=False):
    """
    str -> str -> bool -> list(int)
    
    Input: string (subtext), string (text)
    Output: list of distances between consecutive subtext in text
    
    Print: result information
    """
    index = text.index(subtext)
    subtext_length = len(subtext)
    dist = []
    length = len(text)
    for i in range(length - subtext_length):
        if text[i:i+subtext_length] == subtext:
            dist.append(i - index)
            index = i

    if PRINT: print("The list of distance between " + subtext + ": ", dist[1:])
    
    return dist[1:]

def allGcd(nums, PRINT=False):
    """
    list(int) -> bool -> list(int)
    
    Input: a list of integers (nums)
    Output: a list of gcds between every 2 different num in nums
    
    Print: result list
    """
    gcds = []
    length = len(nums)

    for i in range(length):
        for j in range(i + 1, length):
            gcds.append(math.gcd(nums[i], nums[j]))

    if PRINT: print("The list of gcd's between distances: ", gcds)
    
    return gcds

def everyNthLetters(n, text):
    """
    int -> str -> bool -> list(str)
    
    Input: cyclical length (n), string (text)
    Output: a list of n strings taken from each i*k where i < n and k <= len(text) // n
    
    Print: none
    """
    string_list = []
    length = len(text)
    # Max number of whole string of length n in text
    string_count = length // n
    
    for i in range(n):
        string = ""
        for j in range(string_count):
            string += text[j*n+i]
        string_list.append(string)
        
    return string_list

def frequencyAnalysis(text, PRINT=False):
    """
    str -> bool -> int
    
    Input: string (text)
    Output: shift with highest score
    
    Print: Frequency score for all subkey
    """
    subkeys = string.ascii_uppercase
    result_shift = 0
    highest_score = 0
    if PRINT: print("Subkey:     Frequency score:")
    
    for subkey in subkeys:
        shift = ord(subkey) - 65
        shift_text = ""
        for char in text:
            shift_char = chr((ord(char) - 65 - shift) % 26 + 65)
            shift_text += str(shift_char)
        score = fa.englishFreqMatchScore(shift_text)
        if score > highest_score:
            highest_score = score
            result_shift = shift
        if PRINT: print(f"{subkey}          {score}")
    
    return result_shift

def mostLikelyKey(nth_letters, PRINT=False):
    """
    list(str) -> bool -> str
    
    Input: a list of n strings (nth_letters)
    Output: most likely key
    
    Print: result
    """
    key = ""
    
    for string in nth_letters:
        shift = frequencyAnalysis(string)
        key += str(chr(shift + 65))
    
    if PRINT: print("Potential key found")
    return key

def decrypt(text, key, PRINT=False):
    """
    str -> str -> bool -> str
    
    Input: string to decrypt (text), string used as key (key)
    Output: decrypted string
    
    Print: result
    """
    index = 0
    length = len(text)
    decryption = ""
    key_length = len(key)
    
    for char in text:
        if index == key_length: index = 0
        cipher_ord = ord(char) - 65
        key_ord = ord(key[index]) - 65
        plain_ord = (cipher_ord - key_ord) % 26
        plain_char = chr(plain_ord + 65)
        
        decryption += str(plain_char)
        index += 1
    
    if PRINT: print("Decryption done")
    return decryption

def vigenereBreak(cipher_text, PRINT=False):
    """
    str -> bool -> tuple(str, str)

    Input: encrypted string (cipher_text), boolean value to switch on/off information printing (disabled by default)
    Output: tuple of key, plain text pair

    Print: vigenere attack process information
    """

    print(f"===========================\nDecrypting Vigenere cipher...\n")
    # First trial - compute trigrams frequency to find potential key length
    if PRINT: print("Finding the key length...\nTrial 1 using 3-grams:")
    trigrams = ngramMaxFrequency(3, cipher_text, PRINT)

    # This will most likely to be multiples of t
    dist3 = distanceBetweenSubtext(random.choice(trigrams), cipher_text, PRINT)

    # Get all gcd's between distances
    gcds3 = allGcd(dist3, PRINT)
    multiple1 = min(gcds3)

    if PRINT: print(f"All those gcd's are multiples of {multiple1}, then t is very likely to be {multiple1}!")

    # Second trial - compute pentagrams frequency to verify that t={multiple1}
    if PRINT: print("\nTrial 2 using 5-grams:")
    pentagrams = ngramMaxFrequency(5, cipher_text, PRINT)
    dist5 = distanceBetweenSubtext(random.choice(pentagrams), cipher_text, PRINT)

    # Get all gcd's between distances
    gcds5 = allGcd(dist5, PRINT)
    multiple2 = min(gcds5)
    t = -1

    if multiple1 == multiple2:
        if PRINT: print(f"This further proved that the key length is {multiple1}!")
        t = multiple1
    else:
        if PRINT: print(f"Redo!")

    # Now we know {t}, computer a list for every {t} character in cipher_text
    nth_letters = everyNthLetters(t, cipher_text)

    # Compute for the mostly likely key
    key = mostLikelyKey(nth_letters, PRINT)

    # Decrypt using key
    decryption = decrypt(cipher_text, key, PRINT)

    return (key, decryption)

if __name__ == '__main__':
    print(f"Preparing to initiate a vigenere cipher attack...")
    file_name = input("Enter the encrypted text file name: ")
    file = open(file_name)
    cipher_text = file.read().replace("\n", "")
    file.close()

    answer = input("Would you like to print program process information? Enter (Yes/No): ")
    PRINT = answer.lower() == "yes"

    key, plain_text = vigenereBreak(cipher_text, PRINT)
    print(f"\nThe key is: {key}\nThe plain text is: {plain_text}")