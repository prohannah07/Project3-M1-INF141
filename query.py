import os
import sys
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
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
    token = word_tokenize(query)
    tagged = pos_tag(token)
    tokenized_query = tagged[0][0].lower()
    pos = get_wordnet_pos(tagged[0][1])
    if tokenized_query not in stop_words_final:
        if pos != "":
            lemma = lemmatizer.lemmatize(tokenized_query, pos)
            return lemma


def enter_query():
    print("Enter your query: ")
    q = str(input())
    lem_q = lemmatize_query(q, lemon)
    print("TOKENIZED AND LEMMATIZED QUERY: ", lem_q)
    return lem_q
