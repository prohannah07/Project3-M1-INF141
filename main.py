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

    corpus = sys.argv[1]

    file_directory = json_to_dict(corpus)
    # print(file_directory["0/1"])

    index_file = 'index.txt'
    i = open(index_file, 'w')

    index_json_file = 'index.json'
    ij = open(index_json_file, 'w')

    index.build_index(file_directory, corpus)
    # i.write("hello world")
    index.write_index_to_file(i)
    # print(index.ll_make_list(index.dictionary["have"]))
    # print(index.dict_posting_to_list())
    index.write_index_to_json_file(index_json_file)
    # print(index.dictionary)
    # print(index.dictionary_list)
    print("# VISITED DOCUMENTS: " + str(index.visitedDocuments))
    print("UNIQUE WORDS: " + str(len(index.dictionary)))

    inf_q = 'informatics_q.txt'
    mondego_q = 'mondego_q.txt'
    irvine_q = 'irvine_q.txt'

    inf = open(inf_q, 'w')
    mon = open(mondego_q, 'w')
    irv = open(irvine_q, 'w')

    # inf_query = enter_query()
    # print_first_20_urls(
    #     inf_query, index.dictionary[inf_query], file_directory, inf)

    # mon_query = enter_query()
    # print_first_20_urls(
    #     mon_query, index.dictionary[mon_query], file_directory, mon)

    # irv_query = enter_query()
    # print_first_20_urls(
    #     irv_query, index.dictionary[irv_query], file_directory, irv)

    i.close()
    inf.close()
    mon.close()
    irv.close()

    gui.corpus_path = corpus
    gui.json_to_dict()
    gui.index_to_dict("index.json")
    gui.root.mainloop()
