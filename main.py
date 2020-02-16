import os
import sys

from query import enter_query
from query import stop_words_size
from readJSON import json_to_dict

if __name__ == "__main__":
    print()
    print("Welcome to Hannah and Rey's Search Engine!")
    print()

    corpus = sys.argv[1]

    file_directory = json_to_dict(corpus)
    # print(file_directory["0/1"])

    enter_query()
    stop_words_size()
