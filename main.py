#!/usr/bin/python3
"""  COS 330 Assignment 5 """

import re
import sys
import os,os.path
from Caesar import CaesarAnalyzer

CaesarDecoder = CaesarAnalyzer()
choiceMenu1 = 1
while (choiceMenu1 != '3'):
    print ('---------------------------------------------------------\n\t\t Caesar Cipher Decoder\n---------------------------------------------------------\n')
    print("""------------ Main MENU ------------
1. Brute force 
2. Cryptanalysis
3. Quit
************************************""")
    choiceMenu1 = input("\nType a number corresponding to your choice (1|2|3): ")
    if (choiceMenu1 == '1'):
        path = "/home/kyle/Documents/Year 3/COS 330/Assignments/A5/CaesarDecoder/CaesarText.txt"#input("Enter the path to the cipherText file: ") 
        pathAlpha = "/home/kyle/Documents/Year 3/COS 330/Assignments/A5/CaesarDecoder/alphabets.txt" #input("Enter the path to the alphabets file: ")
        CaesarDecoder.loadCipherTextFile(path)
        CaesarDecoder.loadAlphabets(pathAlpha)
        manualChoice = input("Manually preform bruteforce? (Y|N): ")
        manualChoice = manualChoice.lower()
        if (manualChoice == 'y'):
            CaesarDecoder.bruteForce(True)
        else:
            CaesarDecoder.bruteForce(False)
    elif (choiceMenu1 == '2' ):
        path = "/home/kyle/Documents/Year 3/COS 330/Assignments/A5/CaesarDecoder/CaesarText.txt"#input("Enter the path to the cipherText file: ") 
        pathAlpha = "/home/kyle/Documents/Year 3/COS 330/Assignments/A5/CaesarDecoder/alphabets.txt" #input("Enter the path to the alphabets file: ")
        CaesarDecoder.loadCipherTextFile(path)
        CaesarDecoder.loadAlphabets(pathAlpha)
        print(CaesarDecoder.getRelativeCharacterFreq())