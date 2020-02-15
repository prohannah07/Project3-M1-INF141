import os
import sys
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet

if __name__ == "__main__":
    print("Hello World")
    print()
    print(sys.argv[1])
    # print()

    # print(os.path.isdir(sys.argv[1]))
    # print(os.path.join(sys.argv[1], "0", "1"))
    # print(os.path.isfile(os.path.join(sys.argv[1], "0", "1")))
    # stop words = https://www.ranks.nl/stopwords
    # stop_words = open("stopwords.txt", 'r', encoding='utf8')
    stop_words_path = "stopwords.txt"
    stop_words = open(stop_words_path, 'r', encoding='utf8').read().split('\n')

    all_tokens_frequency = {}

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

    f2 = open(os.path.join(sys.argv[1], "74", "495"), 'r', encoding='utf8')

    soup = BeautifulSoup(f2, 'lxml')
    tokens = word_tokenize(soup.get_text())
    tagged_tokens = pos_tag(tokens)
    print(tokens)
    print(tagged_tokens)

    for word_tag in tagged_tokens:
        token = word_tag[0]
        pos = get_wordnet_pos(word_tag[1])
        if token not in stop_words:
            if pos != "":
                lemma = lemon.lemmatize(token, pos)
                print(token, "---", lemma, "---", pos)

    def computeWordFrequencies(all_tokens_frequency_param):
        tokenMap = {}
        for token in tokenList:
            if (tokenMap.get(token)):
                tokenMap[token] += 1
            else:
                tokenMap[token] = 1
        return tokenMap

    # print(soup.prettify())
    # print("KSAJDKLSADJKLASDJLKAS")
    # for tag in soup.find_all(True):
    #     print(tag.name)
    # corpus = Corpus(sys.argv[1])

    # # for tag in soup.find_all(True):
    # #     print(tag.name)

    # # for tag in soup.find_all(True):
    # #     print(tag.contents)

    # for tag in soup.find_all(True):
    #     print(tag.name + "--------->", tag.contents)

    # for tag in soup.find_all(True):
    #     for i in tag.contents:
    #         print("TEST: ", i)
    #         print(bool(BeautifulSoup(str(i), "html.parser").find()))

    # print(word_tokenize("poop didn't bitch running"))

    # lemon = WordNetLemmatizer()

    # print(lemon.lemmatize("dancing"))
    # print(lemon.lemmatize("dancing", pos="n"))

    # for folder in range(75):
    #     for file in range(500):
    #         filePath = os.path.join(sys.argv[1], str(folder), str(file))
    #         if os.path.isfile(filePath):
    #             f = open(filePath, 'r', encoding='utf8')
    #             soup = BeautifulSoup(f, 'lxml')
    #             print(folder, file)
    #             print(word_tokenize(soup.get_text()))
    #             f.close()
