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


stop_words_path = "stopwords.txt"
stop_words = open(stop_words_path, 'r', encoding='utf8').read().split('\n')

stop_words_final = []
for word in stop_words:
    stop_words_final.extend(word_tokenize(word))

dictionary = {}
visitedDocuments = 0
uniqueWords = 0
lemon = WordNetLemmatizer()


def parseElement(parent, folderNum, fileNum):
    # dictionary is index dictionary
    docID = folderNum + "/" + fileNum
    # global uniqueWords
    for child in parent.contents:
        # print("There is a CHILD Element of " + parent.name)
        # print(type(child))
        if(isinstance(child, bs4.element.NavigableString)):
            # print("This is a string: " + child)
            tokens = word_tokenize(child)
            tagged_tokens = pos_tag(tokens)
            # print(tokens)
            # print(tagged_tokens)
            for word_tag in tagged_tokens:
                token = word_tag[0].lower()
                pos = get_wordnet_pos(word_tag[1])
                if token not in stop_words_final and len(token) > 2:
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
        if(isinstance(child, bs4.element.Tag)):
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
        self.data = data  # Assign data
        self.next = None  # Initialize
        # next as null

# Linked List class


class LinkedList:

    # Function to initialize the Linked
    # List object
    def __init__(self):
        self.head = None


def build_index():
    pass


def index_size(index_dict):
    size = sys.getsizeof(index_dict)
    print("INDEX SIZE ON DISK: ", size, "bytes")
    return size
