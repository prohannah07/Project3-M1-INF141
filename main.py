import os
import sys

from query import enter_query
from query import stop_words_size
from corpus import json_to_dict
# from corpus import print_first_20_urls
from corpus import print_ranked_results
from corpus import retrieve_corpus_data
from corpus import normalize_terms
from corpus import compute_score
import index

if __name__ == "__main__":
    print()
    print("Welcome to Hannah and Rey's Search Engine!")
    print()

    corpus = sys.argv[1]

    file_directory = json_to_dict(corpus)

    index_file = 'index.txt'
    i = open(index_file, 'w')

    index_file = 'PIndex.txt'
    j = open(index_file,'w')

    reference_file = 'Document_Reference.txt'
    ref = open(reference_file,'w')

    index.build_index(file_directory, corpus)

    index.write_index_to_file(i,j)
    i.close()
    j.close()

    index.write_reference_to_file(ref)
    ref.close()
    
    print("# VISITED DOCUMENTS: " + str(index.visitedDocuments))
    print("# INVALID DOCUMENTS: " + str(index.invalidDocuments))
    print("UNIQUE WORDS: " + str(len(index.dictionary)))

    q = 'query.txt'
    q_file =  open(q, 'w')
    while(True):

        query = enter_query() # Dictionary returned Token:Frequency
        query_terms = {"length_norm": 0}
        query_search = {}
        ## dict.clear()
        for token in query:
            index = open(index_file,'r')
            #ref = open(reference_file,'r')
            print("TOKENIZED AND LEMMATIZED QUERY: ", token)
            retrieve_corpus_data(token, query[token], query_terms, query_search, index)
            index.close()
        normalize_terms(query_terms,query_search,reference_file)
        # print("Query Terms")
        # print(query_terms)
        # print("Query Search")
        # print(query_search)
        print("Retrieved URLs")
        print_ranked_results(query_search,file_directory,q_file)

    q_file.close()
