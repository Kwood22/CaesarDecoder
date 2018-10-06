#!/usr/bin/python3
import sys
import os,os.path
import operator
from DictionaryChecker import DictionaryChecker
from collections import deque
class CaesarAnalyzer:

    def __init__(self):
        self.cipherText = ''
        self.alphabets = []
        self.dict = DictionaryChecker()
        self.engLetterFreq = self.initLetterFreq()

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


    def bruteForce(self,isManual):
        # brute force approach 
        # if manual = true user decides what shift and alphabet to use
        choiceBruteForce = '1'
        previousAlphabet = ''
        alphabetCorrectWordCounts = []
        for alphabet in self.alphabets:
            alphabet = alphabet.strip('\n')
            print ("\nCurrent Alphabet: ",alphabet)
            if (isManual):
                #manual bruteforce
                if (choiceBruteForce == '1'):
                    self.bruteForceUsing(alphabet)
                    choiceBruteForce =input("------------ MENU 2 ------------\n1. Try next alphabet\n2. Decode full text using current alphabet with a chosen shift\n3. Return main menu\n************************************ \nType a number corresponding to your choice (1|2|3): ")

                    if (choiceBruteForce == '2'):
                        shift = int(input("\n Input the shift number to decode with: "))
                        self.exportFullDecryptedCipherText(shift,alphabet)
                        break
                else:
                    break
            else: 
                #automatic bruteforce
                alphabetCorrectWordCounts.append(self.bruteForceUsing(alphabet))

        if (isManual == False):
            bestAlphabetIndex = self.findBestAlphabet(alphabetCorrectWordCounts)
            bestAlphabet = self.alphabets[bestAlphabetIndex]
            bestShift = self.findBestShift(alphabetCorrectWordCounts[bestAlphabetIndex])
            bestWordCount = max(alphabetCorrectWordCounts[bestAlphabetIndex])
            print ("\n**********************\n\tResults\n**********************\nBest alphabet: ",bestAlphabet,"\nBest Shift: ",bestShift,"\nBest # Words: ",bestWordCount)
            self.exportFullDecryptedCipherText(bestShift,bestAlphabet)
        elif (choiceBruteForce == '1'):
            choice = input("There are no more alphabets left, Continue (Y)")

    def findBestAlphabet (self , alphabetWordCounts):
        # Find alphabet with best correct word count
        bestCount = 0
        bestIndex = 0
        index = 0
        for alphaCount in alphabetWordCounts:
            if (len(alphaCount)>0):
                if (max(alphaCount) > bestCount):
                    bestCount = max(alphaCount)
                    bestIndex = index
            index += 1
        return bestIndex

    def findBestShift (self, alphabetWordCount):
        # Finds the shift number of an alphabet with the best word count
        bestCount = max(alphabetWordCount)
        return alphabetWordCount.index(bestCount)

    def bruteForceUsing(self, alphabet):
        #print out all decrypted text for a sample trying all combinations of an alphabet
        #Return correct word counts of each combination
        maxShifts = len(alphabet)
        sampleCipherTxt = self.getSampleOfCipherText()
        bestShift = 0 
        shiftNumberCorrectWords = []
        for shift in range(maxShifts):
            shiftedAlphabet = self.rotateAlphabet(alphabet,shift)
            plaintext = self.decryptCipherText(shiftedAlphabet,alphabet,sampleCipherTxt)
            numWords = self.countDictionaryWords(plaintext)
            shiftNumberCorrectWords.append(numWords)
            print("Shift: ",shift," , Decoded: ",plaintext,", #Words: ",numWords)
            
        print("\n")
        return shiftNumberCorrectWords

    def countDictionaryWords (self, plaintext):
        #produce correct word count
        plaintext = plaintext.split(' ')
        return self.dict.getNumRealWords(plaintext)
        

    """
    -----------------
    Freq Analysis
    -----------------
    """

    # Todo: I have implemented it differently to what you have suggested... so the code might end up being usless
    def initLetterFreq(self):
        return ['e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','q','z',4,9,0,1,2,3,5,6,7,8]

    def getCharacterFrequencies(self):
        #Create dictionary of character frequencies
        #order : a-z and 0-9
        letterFreq = [0] * 36
        cipherText = self.cipherText.lower()
        cipherText=cipherText.replace('\n','')
        cipherText=cipherText.replace(' ','')
        for c in cipherText:
            if (c == None):
                break
            if (c.isalnum()):
                if (c.isalpha()):
                    index = ord(c) - ord('a')
                else:
                    print(c)
                    index = 25 + int(c)
                   
                letterFreq[index] += 1
        return self.getSortedLetterArray(letterFreq)
        

    def getSortedLetterArray (self, letterFreq):
        letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']
        
        for i in range(0,35):
            for j in range (0,35):
                if(letterFreq[i]>letterFreq[j]):
                    #swap letters at i and j
                    tempLetter = letters[j]
                    letters[j] = letters[i]
                    letters[i] = tempLetter
                    tempFreq = letterFreq[j]
                    letterFreq[j] = letterFreq[i]
                    letterFreq[i] = tempFreq
        return letters


    def frequencies (self):
        freq = self.getCharacterFrequencies()
        sampleCipherTxt = self.getSampleOfCipherText()
        plaintext = ''
        for word in sampleCipherTxt:
            newWord = []
            for letter in word:
                letter = letter.lower()
                if (letter.isalnum()):
                    index = freq.index(letter)
                    print(letter,index)
                    replacementLetter = self.engLetterFreq[index]
                    newWord.append(replacementLetter)
            print (word," -> ",newWord)
            #plaintext = ''.join(newWord)

        print(plaintext)

    
    def rotateAlphabet(self,alphabet,n):
        #shift key
        return alphabet[n:]+alphabet[:n]

    def exportFullDecryptedCipherText (self, shift,alphabet):
        #export textfile with full decrypted cipher text
        file = open("decoded.txt","w+")
        ciphertext = self.cipherText.split(' ')
        # Sanitise Alphabet
        alphabet = alphabet.strip(' ')
        alphabet = alphabet.strip('\n')
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
                    decodedIndex = ind * (-1)
                    plaintextChars.append(word[decodedIndex]) #extract punctuation from ciphertext word
                else: 
                    plaintextChars.append(alphabet[ind])
            plaintext = ''.join(plaintextChars)
            decryptedSample.append(plaintext)
        
        return ' '.join(decryptedSample) 
