import json
import re
import bs4
import html5lib
from bs4 import BeautifulSoup

import os
import sys
from nltk.stem import WordNetLemmatizer
# from nltk import word_tokenize
from tokenizer import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet
import nltk

from crawler import is_valid

# Stop Words File
stop_words_path = "stopwords.txt"
stop_words = open(stop_words_path, 'r', encoding='utf8').read().split('\n')

stop_words_final = []
for word in stop_words:
    stop_words_final.extend(word_tokenize(word))

dictionary = {}  # Key:Value -> Token:LinkedList<DocID> -> DocIDs are Nodes
visitedDocuments = 0
uniqueWords = 0
lemon = WordNetLemmatizer()  # nltk lemmatizer


def parseElement(parent, folderNum, fileNum):
    # Function takes in a Parent Element and finds the Children Elements
    # FolderNum and FileNum refer to the file that the function is currently being called on
    # Initially (before recursion) the Parent Element is the Document Element (aka the entire HTML code)
    docID = folderNum + "/" + fileNum
    for child in parent.contents:
        # print("There is a CHILD Element of " + parent.name)
        # print(type(child))
        # If child is string we want to tokenize it. Does not have children.
        if(isinstance(child, bs4.element.NavigableString)):
            # print("This is a string: " + child)
            # Outputs Tokens from the given string
            tokens = word_tokenize(child)
            tagged_tokens = pos_tag(tokens)  # Outputs List<Token,POS>
            # print(tokens)
            # print(tagged_tokens)
            # Iterate through (Token, POS) pairs in List
            for word_tag in tagged_tokens:
                token = word_tag[0].lower()  # Lowercases Token
                pos = get_wordnet_pos(word_tag[1])
                if token not in stop_words_final and len(token) > 2:
                    if pos != "":
                        lemma = lemon.lemmatize(token, pos)  # Lemmatizes Token
                        # print(token, "---", lemma, "---", pos)
                        # If Token is in Dictionary AND Posting does not contain current DocID
                        if lemma in dictionary and dictionary[lemma].head.data != docID:
                            currentDoc = Node(docID)  # Create a new DocID
                            # Make current DocID NEXT point to -> Posting
                            currentDoc.next = dictionary[lemma].head
                            # Key:Value -> Token:Posting    # Make current DocID HEAD of Token's Posting
                            dictionary[lemma].head = currentDoc
                        elif lemma not in dictionary:  # If Token is not in Dictionary
                            posting = LinkedList()  # Create a new Posting (LinkedList<DocID>)
                            currentDoc = Node(docID)  # Create a new DocID
                            posting.head = currentDoc  # Point new Posting HEAD -> new  DocID
                            # Key:Value -> Token:Posting
                            dictionary[lemma] = posting
        if(isinstance(child, bs4.element.Tag)):  # If child is Tag we want to see if it has children
            # print("Element Name: " + child.name)
            parseElement(child, folderNum, fileNum)


def get_wordnet_pos(treebank_tag):
    # Function to find part of speech
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
        self.data = data  # Assign data
        self.next = None  # Initialize
        # next as null

# Linked List class


class LinkedList:

    # Function to initialize the Linked
    # List object
    def __init__(self):
        self.head = None


def ll_len(ll):
    # Function finds length of LinkedList
    length = 0
    current = ll.head
    if(current != None):
        length += 1
        while(current.next != None):
            current = current.next
            length += 1
    return length


def build_index(file_directory, corpus_path):
    # Function that parses file_directory (bookingkeepings.json) to find path to HTML Document
    # Then calls functions to parse HTML Doc and go through its contents
    global visitedDocuments
    counter = 0
    for key in file_directory:
        if(counter < 20):
            folder_file_pair = key.split("/")
            folderNum = folder_file_pair[0]
            fileNum = folder_file_pair[1]
            URL = file_directory[key]
            if( is_valid(URL) ):
                ##print("Folder: " + folderNum + "    File: " + fileNum + "   URL: " + URL)
                f = open(os.path.join(corpus_path, folderNum,
                                    fileNum), 'r', encoding='utf8')
                soup = BeautifulSoup(f, 'html5lib') # Parse Current HTML Document
                parseElement(soup, folderNum, fileNum) # A Recursive Function that goes through HTML Document Tags and Text
                visitedDocuments += 1
                counter += 1
            # else:
            #     print("NOT VALID - Folder: " + folderNum + "    File: " + fileNum + "   URL: " + URL)
        else:
            break


def index_size(index_dict):
    size = sys.getsizeof(index_dict)
    print("INDEX SIZE ON DISK: ", size, "bytes")
    return size


def index_size_final():
    size = sys.getsizeof(dictionary)
    print("INDEX SIZE ON DISK: ", str(size / 1000), "KB")
    return size / 1000


def write_index_to_file(file):
    for key in dictionary:
        file.write(key + "\n")
        current = dictionary[key].head
        file.write(current.data + "\n")
        while(current.next != None):
            current = current.next
            file.write(current.data + "\n")
            # print(current.data)
        file.write("END" + "\n")
