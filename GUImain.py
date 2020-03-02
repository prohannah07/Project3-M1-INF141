import os
import sys
from tkinter import *

import gui
from query import enter_query
from query import stop_words_size
from corpus import json_to_dict
from corpus import print_first_20_urls
import index

if __name__ == "__main__":
    print()
    print("Welcome to Hannah and Rey's Search Engine!")
    print()

    corpus_path = sys.argv[1]
    index_file = open("PIndex.txt", 'r')
    q = 'query.txt'
    q_file = open(q, 'w')
    # index_file = os.path.join(sys.argv[2], "index.txt")
    # PIndex_file = os.path.join(sys.argv[2], "PIndex.txt")
    # reference_file = os.path.join(sys.argv[2], "Document_Reference.txt")

    # file_directory = json_to_dict(corpus_path)

    gui.corpus_path = corpus_path
    gui.index_file = index_file
    gui.q_file = q_file
    gui.json_to_dict()
    # gui.index_to_dict("index.json")
    gui.root.mainloop()
    index_file.close()
    q_file.close()
