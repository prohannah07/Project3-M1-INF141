import os
import sys
from bs4 import BeautifulSoup

if __name__ == "__main__":
    print("Hello World")
    print(sys.argv[1])
    print()

    print(os.path.isdir(sys.argv[1]))
    print(os.path.join(sys.argv[1], "0", "1"))
    print(os.path.isfile(os.path.join(sys.argv[1], "0", "1")))

    f = open(os.path.join(sys.argv[1], "0", "1"), 'r', encoding='utf8')

    soup = BeautifulSoup(f, 'lxml')
    print(soup.prettify())
    print("KSAJDKLSADJKLASDJLKAS")
    for tag in soup.find_all(True):
        print(tag.name)
    # corpus = Corpus(sys.argv[1])
