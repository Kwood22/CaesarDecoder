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
        path = "/home/kyle/Documents/Year 3/COS 330/Assignments/A5/CaesarText.txt"#input("Enter the path to the cipherText file: ") 
        pathAlpha = "/home/kyle/Documents/Year 3/COS 330/Assignments/A5/alphabets.txt" #input("Enter the path to the alphabets file: ")
        CaesarDecoder.loadCipherTextFile(path)
        CaesarDecoder.loadAlphabets(pathAlpha)
        choiceBruteForce = '1'
        alphabets = CaesarDecoder.getAlphabets()
        previousAlphabet = ''
        for alphabet in alphabets:
            if (choiceBruteForce == '1'):
                CaesarDecoder.bruteForce(alphabet)
                choiceBruteForce =input("------------ MENU ------------\n1. Try next alphabet\n2. Decode full text using current alphabet\n3. Return main menu\n************************************ \nType a number corresponding to your choice (1|2|3): ")
                previousAlphabet = alphabet
            elif (choiceBruteForce == '2'):
                shift = int(input("\n Input the shift number to decode with: "))
                CaesarDecoder.exportFullDecryptedCipherText(shift,previousAlphabet)
                break
            else:
                break
        if (choiceBruteForce == '1'):
            print("There are no more alphabets left")
            choiceBruteForce =input("------------ MENU ------------\n1. Try next alphabet\n2. Decode full text using current alphabet\n3. Return main menu\n************************************ \nType a number corresponding to your choice (1|2|3): ")
    elif (choiceMenu1 == '2' ):
        break