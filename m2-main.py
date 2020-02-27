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

    # print(file_directory["0/273"])

    print(is_valid(file_directory["0/273"]))
