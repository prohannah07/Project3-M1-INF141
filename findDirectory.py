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

    soup = BeautifulSoup(os.path.join(sys.argv[1], "0", "1"), 'html.parser')
    print(soup.get_text())
    # corpus = Corpus(sys.argv[1])
