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
from math import log10

from crawler import is_valid

# Stop Words File
stop_words_path = "stopwords.txt"
stop_words = open(stop_words_path, 'r', encoding='utf8').read().split('\n')

stop_words_final = []
for word in stop_words:
    stop_words_final.extend(word_tokenize(word))

dictionary = {}  # Key:Value -> Token:LinkedList<DocID> -> DocIDs are Nodes
tagWeightDict = {"title": 5,"h1": 4, "h2": 3, "h3": 2, "strong": 1}
excludedParentTags = set(["script","style","head"])
visitedDocuments = 0
invalidDocuments = 0
uniqueWords = 0
lemon = WordNetLemmatizer()  # nltk lemmatizer


def parse_element(parent, folderNum, fileNum):
    # Function takes in a Parent Element and finds the Children Elements
    # FolderNum and FileNum refer to the file that the function is currently being called on
    # Initially (before recursion) the Parent Element is the Document Element (aka the entire HTML code)
    global excludedParentTags
    docID = folderNum + "/" + fileNum
    for child in parent.contents:
        # If child is string we want to tokenize it. Does not have children.
        if(isinstance(child, bs4.element.NavigableString) and parent.name not in excludedParentTags):
            # Outputs Tokens from the given string
            # print("This Element is a Child of " + parent.name)
            # print(child)
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
                        if lemma in dictionary and dictionary[lemma].head.docID != docID: # If Token is in Dictionary AND Posting does not contain current DocID
                            posting = dictionary[lemma]
                            currentDoc = Node(docID)  # Create a new DocID
                            check_tag_weight(parent.name,currentDoc)
                            currentDoc.next = posting.head # Make current DocID NEXT point to -> Posting
                            posting.head = currentDoc # Key:Value -> Token:Posting    # Make current DocID HEAD of Token's Posting
                            posting.len += 1
                        elif lemma in dictionary: # If Token is in Dictionary AND Posting does contain current DocID
                            currentDoc = dictionary[lemma].head
                            check_tag_weight(parent.name,currentDoc)
                            currentDoc.count += 1
                            currentDoc.tf = compute_weighted_term_frequency(currentDoc.count)
                        elif lemma not in dictionary:  # If Token is not in Dictionary
                            posting = LinkedList()  # Create a new Posting (LinkedList<DocID>)
                            currentDoc = Node(docID)  # Create a new DocID
                            check_tag_weight(parent.name,currentDoc)
                            posting.head = currentDoc  # Point new Posting HEAD -> new  DocID
                            posting.len += 1
                            dictionary[lemma] = posting # Key:Value -> Token:Posting
        if(isinstance(child, bs4.element.Tag)):  # If child is Tag we want to see if it has children
            # print("Element Name: " + child.name)
            parse_element(child, folderNum, fileNum)

def check_tag_weight(parent_tag, currentDoc):
    global tagWeightDict
    if parent_tag in tagWeightDict:
        if currentDoc.tagWeight < tagWeightDict[parent_tag]:
            currentDoc.tagWeight = tagWeightDict[parent_tag]
            currentDoc.priorityTag = parent_tag

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
    def __init__(self, docID):
        self.docID = docID  # Assign data
        self.count = 1
        self.tagWeight = 0
        self.priorityTag = "None"
        self.tf = compute_weighted_term_frequency(self.count)
        self.tf_idf = 0
        self.next = None  # Initialize
        # next as null

# Linked List class


class LinkedList:

    # Function to initialize the Linked
    # List object
    def __init__(self):
        self.head = None
        self.idf = 0
        self.len = 0


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
    global invalidDocuments
    counter = 0
    for key in file_directory:
        if(counter < 50):
            folder_file_pair = key.split("/")
            folderNum = folder_file_pair[0]
            fileNum = folder_file_pair[1]
            URL = file_directory[key]
            if( is_valid(URL) ):
                print("Folder: " + folderNum + "    File: " + fileNum + "   URL: " + URL)
                f = open(os.path.join(corpus_path, folderNum,
                                    fileNum), 'r', encoding='utf8')
                soup = BeautifulSoup(f, 'html5lib') # Parse Current HTML Document
                parse_element(soup, folderNum, fileNum) # A Recursive Function that goes through HTML Document Tags and Text
                visitedDocuments += 1
                counter += 1
            else:
                print("NOT VALID - Folder: " + folderNum + "    File: " + fileNum + "   URL: " + URL)
                invalidDocuments += 1
        else:
            break

def build_test(file_directory, corpus_path):
    global visitedDocuments
    global invalidDocuments
    fileNum = "112"
    folderNum = "0"
    f = open(os.path.join(corpus_path, folderNum,
                                    fileNum), 'r', encoding='utf8')
    soup = BeautifulSoup(f, 'html5lib') # Parse Current HTML Document
    parse_element(soup, folderNum, fileNum) # A Recursive Function that goes through HTML Document Tags and Text
    visitedDocuments += 1


def compute_inverse_document_frequency(token, posting, total_documents):
    idf = log10(total_documents/posting.len)
    return idf


def compute_weighted_term_frequency(count):
    tf = 1 + log10(count)
    return tf


def compute_tf_idf(term_frequency, inverse_document_frequency):
    tf_idf = term_frequency * inverse_document_frequency
    return tf_idf


def index_size(index_dict):
    size = sys.getsizeof(index_dict)
    print("INDEX SIZE ON DISK: ", size, "bytes")
    return size


def index_size_final():
    size = sys.getsizeof(dictionary)
    print("INDEX SIZE ON DISK: ", str(size / 1000), "KB")
    return size / 1000


def write_index_to_file(file):
    global visitedDocuments
    total_documents = visitedDocuments
    for key in dictionary:
        posting = dictionary[key]
        current = dictionary[key].head
        file.write(key)
        posting.idf = compute_inverse_document_frequency(key,dictionary[key],total_documents)
        current.tf_idf = compute_tf_idf(current.tf,posting.idf)
        file.write("    Inverse Document Frequency: " + str(posting.idf) + "\n")
        file.write("DocID: " + current.docID + "  Count: " + str(current.count) + "   Priority: " + current.priorityTag + "   Weight: " + str(current.tagWeight) + "    Term Frequency: " + str(current.tf) + "   tf-idf: " + str(current.tf_idf) + "\n")
        while(current.next != None):
            current = current.next
            current.tf_idf = compute_tf_idf(current.tf,posting.idf)
            file.write("DocID: " + current.docID + "  Count: " + str(current.count) + "   Priority: " + current.priorityTag + "   Weight: " + str(current.tagWeight) + "   Term Frequency: " + str(current.tf) + "   tf-idf: " + str(current.tf_idf) + "\n")
        file.write("END" + "\n")
