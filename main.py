import json
from bs4 import BeautifulSoup


if __name__ == "__main__":

    with open("../WEBPAGES_CLEAN/bookkeeping.json") as bookkeeping:
        data = json.load(bookkeeping)

    for key in data:
        folder_file_pair = key.split("/")
        folderNum = folder_file_pair[0]
        fileNum = folder_file_pair[1]
        URL = data[key]
        print("Folder: " + folderNum + "    File: " + fileNum + "   URL: " + URL)
        f = open("../WEBPAGES_CLEAN/" + folderNum + "/" + fileNum, 'r', encoding='utf8')
        # print(f)
        soup = BeautifulSoup(f, 'lxml-xml')
        # print(soup.prettify())
        for tag in soup.find_all(True):
            print(tag.name)