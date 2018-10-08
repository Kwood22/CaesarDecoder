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
            if (isManual): 
                print ("\nCurrent Alphabet: ",alphabet)
            if (isManual):
                #manual bruteforce
                if (choiceBruteForce == '1'):
                    self.bruteForceUsing(alphabet,isManual)
                    choiceBruteForce =input("------------ MENU 2 ------------\n1. Try next alphabet\n2. Decode full text using current alphabet with a chosen shift\n3. Return main menu\n************************************ \nType a number corresponding to your choice (1|2|3): ")

                    if (choiceBruteForce == '2'):
                        shift = int(input("\n Input the shift number to decode with: "))
                        self.exportFullDecryptedCipherText(shift,alphabet)
                        break
                else:
                    break
            else: 
                #automatic bruteforce
                alphabetCorrectWordCounts.append(self.bruteForceUsing(alphabet,isManual))

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

    def bruteForceUsing(self, alphabet,isManual):
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
            if (isManual):
                print("Shift: ",shift," , Decoded: ",plaintext,", #Words: ",numWords)
        if (isManual):    
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

    def initLetterFreq(self):
        return {'e':0.12702,'t':0.09056,'a':0.08167,'o':0.07507,'i':0.06966,'n':0.06749,'s':0.06327,'h':0.06094,'r':0.05987,'d':0.04253,'l':0.04025,'c':0.02782,'u':0.02758,'m':0.02406,'w':0.02360,'f':0.02228,'g':0.02015,'y':0.01974,'p':0.01929,'b':0.01492,'v':0.00978,'k':0.00772,'j':0.00153,'x':0.00150,'q':0.00095,'z':0.00074}
        
    def getRelativeCharacterFreq (self):
        cipherText = self.cipherText.lower()
        cipherText=cipherText.replace('\n','')
        cipherText=cipherText.replace(' ','')
        listOfCharacters={}
        numLetters = 0
        for letter in cipherText:
            if (letter.isalnum()):
                numLetters += 1
                if letter in listOfCharacters.keys():
                    listOfCharacters[letter]+=1
                else:
                    listOfCharacters[letter]=1
        for k,v in listOfCharacters.items():
            listOfCharacters[k] = (v/numLetters)

        sorted_by_value = sorted(listOfCharacters.items(), key=lambda kv: kv[1],reverse=True)
        return dict(sorted_by_value)

    def cryptAnalysis(self):
        engLetterFreq = self.initLetterFreq()
        cipherTextFreq = self.getRelativeCharacterFreq()
        sampleCipherText = self.getSampleOfCipherText()
        result = self.getCryptAnalysisShift(engLetterFreq, cipherTextFreq, sampleCipherText)
        if (result['shiftValue'] != -1):
            self.exportFullDecryptedCipherText(62 - result['shiftValue'], result['alphabet'])
        # end if
    # end cryptAnalysis

    def getCryptAnalysisShift(self, engLetterFreq, cipherTextFreq, sampleCipherText):
        for alphabet in self.alphabets:
            for engChar in engLetterFreq:
                for cipherChar in cipherTextFreq:
                    shiftValue = self.getShiftValue(engChar, cipherChar, alphabet)
                    isValidWord = True
                    for sampleWord in sampleCipherText:
                        word = self.decipherWord(sampleWord, shiftValue, alphabet)
                        if (self.dict.check(word) == False):                            
                            isValidWord = False
                        # end if
                    # end for
                    if (isValidWord == True):
                        return { 'shiftValue': shiftValue, 'alphabet': alphabet } 
                    # end if
                # end for
            # end for
        # end for
        return { 'shiftValue': -1, 'alphabet': None }
    # end cryptAnalysisShift

    def getShiftValue(self, engChar, cipherChar, alphabet):
        engCharIndex = -1
        counter = 0
        for alphabetChar in alphabet:
            if (alphabetChar == engChar):
                engCharIndex = counter
            # end if
            counter += 1
        # end for

        cipherCharIndex = -1
        counter = 0
        for alphabetChar in alphabet:
            if (alphabetChar == cipherChar):
                cipherCharIndex = counter
            # end if
            counter += 1
        # end for

        # set all shifts to right shift
        if ((engCharIndex - cipherCharIndex) < 0):
            return (62 - cipherCharIndex + engCharIndex)
        else:
            return (engCharIndex - cipherCharIndex)
    # getShiftValue

    def decipherWord(self, sampleWord, shiftValue, alphabet):
        plainText = ''
        for char in sampleWord:
            if (char.isalnum()):
                count = 0
                for alphaChar in alphabet:
                    if (char == alphaChar):
                        charIndex = count
                    # end if
                    count += 1
                # end for
                shiftCharIndex = charIndex + shiftValue
                if (shiftCharIndex > 61):   # if overflow past alphabet
                    plainText += alphabet[shiftCharIndex - 62]  # if value is 62, then it is value 0
                else:
                    plainText += alphabet[shiftCharIndex]
                # end if
            # end if
        # end for
        return plainText
    # end decipherWord
    
    def rotateAlphabet(self, alphabet, n):
        #shift key
        return alphabet[n:]+alphabet[:n]
    # end rotateAlphabet

    def exportFullDecryptedCipherText (self, shift,alphabet):
        #export textfile with full decrypted cipher text
        file = open("decoded.txt","w+")
        ciphertext = self.cipherText.split(' ')
        # Sanitise Alphabet
        alphabet = alphabet.strip(' ')
        alphabet = alphabet.strip('\n')
        shiftedAlphabet = self.rotateAlphabet(alphabet, shift)
        file.write( self.decryptCipherText(shiftedAlphabet, alphabet, ciphertext))
        print ("\n**Successfully created decoded.txt with decoded text**\n")
        file.close()
        input("Continue (Y): ")
    # end exportFullDecryptedCipherText

    def decryptCipherText(self, shiftedAlphabet, alphabet, cipherText): 
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
        # end for
        return ' '.join(decryptedSample) 
    # end decryptCipherText