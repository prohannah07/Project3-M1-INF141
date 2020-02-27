import os
import sys

from crawler import is_valid
from corpus import json_to_dict

if __name__ == "__main__":
    print()
    print("Welcome to Hannah and Rey's Search Engine!")
    print()

    corpus = sys.argv[1]

    file_directory = json_to_dict(corpus)

    # print(is_valid(file_directory["9/98"]))
    valid_urls = []

    for key in file_directory:
        if is_valid(file_directory[key]):
            # print(key + ": " + file_directory[key])
            valid_urls.append(key)

    print()
    print()
    print("UNCHECKED: " + str(len(file_directory)))
    print("CHECKED: " + str(len(valid_urls)))
    print("difference: " + str(len(file_directory) - len(valid_urls)))
    # print(is_valid(file_directory["0/273"]))
