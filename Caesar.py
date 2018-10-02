#!/usr/bin/python3
import sys
import os,os.path
from collections import deque
class CaesarAnalyzer:

    def __init__(self):
        self.cipherText = ''
        self.alphabets = []

    def loadCipherTextFile (self,cipherTextFileName):
        if (os.path.exists(cipherTextFileName)==False): 
            print("Error: path is invalid")
            return -1
        else:                
            with open(cipherTextFileName, 'r') as cipherFile:
                self.cipherText = cipherFile.read()
            return 1

    def loadAlphabets (self,alphabetsPath):
        if (os.path.exists(alphabetsPath)==False): 
            print("Error: path is invalid")
            return -1
        else:                
            with open(alphabetsPath, 'r') as alphabetsFile:
                self.alphabets = alphabetsFile.readlines()
            return 1
        
    def printLoadedFile (self):
        print(self.cipherText)

    def getCharacterFrequencies(self):
        #Create dictionary of character frequencies
        dict = {}
        for c in self.cipherText:
            keys = dict.keys()
            if c in keys:
                dict[c] += 1
            else:
                dict[c] = 1
        return dict

    def getSampleOfCipherText (self):
        # get the first 100 characters
        if (len(self.cipherText) > 100 ):
            sample = self.cipherText [0:100]
            sample = sample.strip('\n')
            return sample.split()
        else:
            return self.cipherText

    def getAlphabets(self):
        return self.alphabets


    def bruteForce(self):
        choiceBruteForce = '1'
        previousAlphabet = ''
        for alphabet in self.alphabets:
            alphabet = alphabet.strip('\n')
            print ("\nCurrent Alphabet: ",alphabet)
            if (choiceBruteForce == '1'):
                self.bruteForceUsing(alphabet)
                choiceBruteForce =input("------------ MENU ------------\n1. Try next alphabet\n2. Decode full text using current alphabet\n3. Return main menu\n************************************ \nType a number corresponding to your choice (1|2|3): ")
                previousAlphabet = alphabet
            elif (choiceBruteForce == '2'):
                shift = int(input("\n Input the shift number to decode with: "))
                self.exportFullDecryptedCipherText(shift,previousAlphabet)
                break
            else:
                break
        if (choiceBruteForce == '1'):
            choice = input("There are no more alphabets left, Continue (Y)")

    def bruteForceUsing(self, alphabet):
        #print out all decrypted text for a sample trying all combinations of an alphabet
        maxShifts = len(alphabet)
        sampleCipherTxt = self.getSampleOfCipherText()
        for shift in range(maxShifts):
            shiftedAlphabet = self.rotateAlphabet(alphabet,shift)
            plaintext = ''
            print("Shift: ",shift," , Decoded: ",self.decryptCipherText(shiftedAlphabet,alphabet,sampleCipherTxt))
        print("\n")

    def rotateAlphabet(self,alphabet,n):
        return alphabet[n:]+alphabet[:n]

    def exportFullDecryptedCipherText (self, shift,alphabet):
        file = open("decoded.txt","w+")
        ciphertext = self.cipherText.split(' ')
        shiftedAlphabet = self.rotateAlphabet(alphabet,shift)
        file.write( self.decryptCipherText(shiftedAlphabet,alphabet,ciphertext))
        print ("\n**Successfully created decoded.txt with decoded text**\n")
        file.close()
        input("Continue (Y): ")

    def decryptCipherText (self, shiftedAlphabet, alphabet, cipherText): 
        plaintext = ''
        decryptedSample = []
        for word in cipherText:
            plaintextCoords = []
            plaintextChars = []
            indx = 0
            for ch in word:
                if (ch.isalnum()):
                    plaintextCoords.append(shiftedAlphabet.find(ch))
                else:
                    encodedIndex = indx * (-1)
                    plaintextCoords.append(encodedIndex) #store index of punctuation in cipher text as neg number
                indx += 1
            for ind in plaintextCoords:
                if (ind < 0):
                    decodedIndex = ind*-1
                    plaintextChars.append(word[decodedIndex]) #extract punctuation fron ciphertext word
                else: 
                    plaintextChars.append(alphabet[ind])
            plaintext = ''.join(plaintextChars)
            decryptedSample.append(plaintext)
        
        return ' '.join(decryptedSample) 
