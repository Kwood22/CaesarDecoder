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
    print("""********** Caesar Cipher Decoder **********\n
------------ MENU ------------
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
        CaesarDecoder.bruteForce()
    elif (choiceMenu1 == '2' ):
        break