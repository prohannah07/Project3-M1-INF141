import json
import nltk
import re
import bs4
import html5lib
from bs4 import BeautifulSoup


def parseElement(parent):
    for child in parent.contents:
        print("There is a CHILD Element of " + parent.name)
        print(type(child))
        if( isinstance(child, bs4.element.NavigableString) ):
            print("This is a string: " + child)
        if( isinstance(child, bs4.element.Tag) ):
            print("Element Name: " + child.name)
            parseElement(child)


if __name__ == "__main__":

    with open("../WEBPAGES_CLEAN/bookkeeping.json") as bookkeeping:
        data = json.load(bookkeeping)

    for key in data:
        folder_file_pair = key.split("/")
        folderNum = folder_file_pair[0]
        fileNum = folder_file_pair[1]
        URL = data[key]
        print("Folder: " + folderNum + "    File: " + fileNum + "   URL: " + URL)
        f = open("../WEBPAGES_CLEAN/" + folderNum + "/" + fileNum, 'r', encoding='utf8')
        # f = open("../WEBPAGES_CLEAN/" + "0" + "/" + "2", 'r', encoding='utf8')
        soup = BeautifulSoup(f, 'html5lib')
        # print(soup)
        parseElement(soup)
 

            