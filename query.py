import os
import sys
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
#from nltk import word_tokenize
from tokenizer import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet

stop_words_path = "stopwords.txt"
stop_words = open(stop_words_path, 'r', encoding='utf8').read().split('\n')

stop_words_final = []
for word in stop_words:
    stop_words_final.extend(word_tokenize(word))

lemon = WordNetLemmatizer()


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


def lemmatize_query(query, lemmatizer):
    query_tokens = {}
    token = word_tokenize(query)
    tagged = pos_tag(token)
    for word_tag in tagged:
        token = word_tag[0].lower()  # Lowercases Token
        pos = get_wordnet_pos(word_tag[1])
        if token not in stop_words_final and len(token) > 2:
            if pos != "":
                lemma = lemmatizer.lemmatize(token, pos)  # Lemmatizes Token
                if lemma not in query_tokens:
                    # print("Added Token: " + lemma)
                    query_tokens[lemma] = 1
                else:
                    # print("Plus one frequency for: " + lemma)
                    query_tokens[lemma] = query_tokens[lemma] + 1
    return query_tokens


def enter_query():
    print("Enter your query: ")
    q = str(input())
    lem_query = lemmatize_query(q, lemon)
    return lem_query


def lemon_query(q):
    lem_query = lemmatize_query(q, lemon)
    return lem_query


def stop_words_size():
    size = sys.getsizeof(stop_words_final)
    print("stop words size: ", size, "bytes")
    return size
