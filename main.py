import json
import re
import bs4
import html5lib
from bs4 import BeautifulSoup

import os
import sys
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')


def parseElement(parent, folderNum, fileNum):
    docID = folderNum+"/"+fileNum
    global uniqueWords
    for child in parent.contents:
        # print("There is a CHILD Element of " + parent.name)
        # print(type(child))
        if( isinstance(child, bs4.element.NavigableString) ):
            # print("This is a string: " + child)
            tokens = word_tokenize(child)
            tagged_tokens = pos_tag(tokens)
            # print(tokens)
            # print(tagged_tokens)
            for word_tag in tagged_tokens:
                token = word_tag[0]
                pos = get_wordnet_pos(word_tag[1])
                if token not in stop_words and len(token) > 2:
                    if pos != "":
                        lemma = lemon.lemmatize(token, pos)
                        # print(token, "---", lemma, "---", pos)
                        if lemma in dictionary and dictionary[lemma].head.data != docID:
                            currentDoc = Node(docID)
                            currentDoc.next = dictionary[lemma].head
                            dictionary[lemma].head = currentDoc
                        elif lemma not in dictionary:
                            posting = LinkedList()
                            currentDoc = Node(docID)
                            posting.head = currentDoc
                            dictionary[lemma] = posting
        if( isinstance(child, bs4.element.Tag) ):
            # print("Element Name: " + child.name)
            parseElement(child, folderNum, fileNum)

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    elif treebank_tag == "CD":
        return wordnet.NOUN
    else:
        return ""


# Node class 
class Node: 

	# Function to initialize the node object 
	def __init__(self, data): 
		self.data = data # Assign data 
		self.next = None # Initialize 
						# next as null 

# Linked List class 
class LinkedList: 
	
	# Function to initialize the Linked 
	# List object 
	def __init__(self): 
		self.head = None

if __name__ == "__main__":



    stop_words_path = "stopwords.txt"
    stop_words = open(stop_words_path, 'r', encoding='utf8').read().split('\n')

    dictionary = {}
    visitedDocuments = 0
    uniqueWords = 0
    lemon = WordNetLemmatizer()


    counter = 0

    with open("../WEBPAGES_CLEAN/bookkeeping.json") as bookkeeping:
        data = json.load(bookkeeping)

    for key in data:
        if( counter < 10 ):
            folder_file_pair = key.split("/")
            folderNum = folder_file_pair[0]
            fileNum = folder_file_pair[1]
            URL = data[key]
            print("Folder: " + folderNum + "    File: " + fileNum + "   URL: " + URL)
            f = open("../WEBPAGES_CLEAN/" + folderNum + "/" + fileNum, 'r', encoding='utf8')
            soup = BeautifulSoup(f, 'html5lib')
            parseElement(soup, folderNum, fileNum)
            visitedDocuments += 1
            counter += 1
        else:
            break

        #####TESTING PURPOSES ONLY#####
        # folderNum = "0"
        # fileNum = "2"
        # f = open("../WEBPAGES_CLEAN/" + folderNum + "/" + fileNum, 'r', encoding='utf8')
        # g = open("../WEBPAGES_CLEAN/0/8", 'r', encoding='utf8')
        # soup = BeautifulSoup(f, 'html5lib')
        # parseElement(soup, folderNum, fileNum)


        # folderNum1 = "0"
        # fileNum1 = "8"

        # soup = BeautifulSoup(g, 'html5lib')
        # parseElement(soup, folderNum1, fileNum1)
        #####TESTING PURPOSES ONLY#####

    for key in dictionary.keys():
        uniqueWords += 1
        print("Key: " + key)
        currentNode = dictionary[key].head
        while(currentNode != None):
            print("Document: " + currentNode.data)
            currentNode = currentNode.next

    print("Number of Visited Documents: " + str(visitedDocuments))
    print("Number of Unique Words: " + str(uniqueWords))

 
