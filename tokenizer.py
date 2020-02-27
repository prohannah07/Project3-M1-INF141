from urllib.parse import urlparse
from bs4 import BeautifulSoup


def word_tokenize(text_block):
    '''
    Hannah's tokenizer from project 1.
    in our code, a "WORD" is any sequence of alphanumeric characters that
    is greater than the length of 2, any string less than the length of 2
    is not considered a WORD
    '''
    tokenList = []
    token = []  # v2
    for char in text_block:
        if (char == ''):
            break
        elif (char.isalnum() and ((97 <= ord(char) <= 122) or (65 <= ord(char) <= 90) or (48 <= ord(char) <= 57))):
            token.append(char.lower())  # v2
        else:
            joinedToken = "".join(token)  # v2
            if (joinedToken and len(joinedToken) > 2):
                tokenList.append(joinedToken)  # tokenList.append(token)
            token = []
    return tokenList
