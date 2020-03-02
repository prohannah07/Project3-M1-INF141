from tkinter import *
from functools import partial
import json
import os
from bs4 import BeautifulSoup
import bs4

from query import lemon_query
from corpus import print_ranked_results
from corpus import retrieve_corpus_data
from corpus import normalize_terms
from corpus import compute_score
import index

corpus_path = ""
index_file = ""
# index = {}
file_directory = {}
retrieved_docIDs = []
excludedParentTags = set(["script", "style", "head"])


def json_to_dict():
    global file_directory
    corpus_json = os.path.join(corpus_path, "bookkeeping.json")

    with open(corpus_json, 'r', encoding='utf8') as f:
        file_directory = json.load(f)


def index_to_dict(index_path):
    global index

    with open(index_path, 'r', encoding='utf8') as f:
        index = json.load(f)

# def handle_query(entry, no_match_label):


def handle_query():
    global retrieved_docIDs
    global index_file
    # index_file.seek(0)

    query = search_entry.get().lower()
    lemonized_query = lemon_query(query)

    query_terms = {"length_norm": 0}
    query_search = {}

    for token in lemonized_query:
        # index_file = open("PIndex.txt", 'r')
        print("TOKENIZED AND LEMMATIZED QUERY: ", token)
        retrieve_corpus_data(
            token, lemonized_query[token], query_terms, query_search, index_file)
        index_file.seek(0)
        # index_file.close()
    normalize_terms(query_terms, query_search, "Document_Reference.txt")

    q = 'query.txt'
    q_file = open(q, 'w')
    print("Retrieved URLs")
    retrieved_docIDs = print_ranked_results(
        query_search, file_directory, q_file)
    q_file.close()

    if query == "":
        print("TYPE SOMETHING!")
    elif len(retrieved_docIDs) == 0:
        noMatchLabel.grid()
        search_results.delete(0, END)
        print("No Matches")
    else:
        noMatchLabel.grid_remove()
        search_results.delete(0, END)

        for posting in retrieved_docIDs:
            print(file_directory[posting])
        make_labels_for_urls(retrieved_docIDs)


def make_labels_for_urls(index_query):
    title_row = 0
    url_row = 1
    desc_row = 2
    space_row = 3
    for posting in index_query:
        if title_row < 72 and url_row < 72 and desc_row < 72 and space_row < 72:
            title = get_url_title(posting)
            desc = get_url_description(posting)
            # get_better_description(posting)
            # Label(bottomFrame, text="title: " + title).grid(row=title_row)
            # Label(bottomFrame, text=file_directory[posting]).grid(row=url_row)
            search_results.insert(title_row, title)
            search_results.itemconfig(title_row, fg="purple")

            search_results.insert(url_row, file_directory[posting])
            search_results.itemconfig(url_row, fg="sky blue")

            search_results.insert(desc_row, desc)
            search_results.itemconfig(desc_row, fg="black")

            search_results.insert(
                space_row, "--------------------------------------------------------------------------------")

            title_row += 4
            url_row += 4
            desc_row += 4
            space_row += 4


def get_url_title(posting):
    folder = posting.split("/")[0]
    file = posting.split("/")[1]

    f = open(os.path.join(sys.argv[1], folder, file), 'r', encoding='utf8')

    soup = BeautifulSoup(f, 'lxml')
    title = soup.title
    if title == "":
        print("NO TITLE")
        return "NO TITLE"
    else:
        print(title.string)
        return title.string


def get_url_description(posting):
    folder = posting.split("/")[0]
    file = posting.split("/")[1]

    f = open(os.path.join(sys.argv[1], folder, file), 'r', encoding='utf8')

    soup = BeautifulSoup(f, 'lxml')

    desc_list = []
    for tags in soup.find_all("meta"):
        if tags.get('content') is not None and "text/html" not in tags.get('content') and "text/css" not in tags.get('content') and "width=device-width" not in tags.get('content'):
            print(tags.get('content'))
            print(tags)
            desc_list.append(tags.get('content'))

    text = soup.get_text().strip().split('\n')
    if len(text) == 0:
        print("NO DESCRIPTION")
        return "NO DESCRIPTION"
    else:
        # print(' '.join(text)[0:100].strip(" \n"))
        # print(desc_list)
        # print(text)
        # print(' '.join(text)[0:300])
        desc_list.extend(text)
        # print(desc_list)
        return ' '.join(desc_list)[0:500].strip()


def get_better_description(posting):
    global excludedParentTags

    folder = posting.split("/")[0]
    file = posting.split("/")[1]

    f = open(os.path.join(sys.argv[1], folder, file), 'r', encoding='utf8')

    soup = BeautifulSoup(f, 'lxml')

    for tags in soup.find_all("meta"):
        print(tags.get('content'))
        print(tags)



#  main window
root = Tk()
root.title("Rey and Hannah's Search Engine")

#  top Frame
topFrame = Frame()
topFrame.pack()

#  Title Label
theLabel = Label(
    topFrame, text="Rey and Hannah's Search Engine!", font=(None, 40), borderwidth=20, relief=FLAT, fg="purple")
theLabel.grid(row=0, columnspan=2)

#  No Matching Results Label
noMatchLabel = Label(topFrame, text="No Matches", fg="red")
noMatchLabel.grid(row=2, columnspan=2)
noMatchLabel.grid_remove()

#  Search Bar
search_entry = Entry(topFrame, width=50, borderwidth=7,
                     relief=FLAT, highlightcolor="purple", highlightbackground="purple")
search_entry.grid(row=1, column=0, sticky=E)

#  Search Button
# handle_query_with_arg = partial(handle_query, search_entry, noMatchLabel)
# command=handle_query, height=2, width=10)
search_button = Button(topFrame, text="Search", height=2,
                       width=10, command=handle_query)
search_button.grid(row=1, column=1, sticky=W)
# search_button.bind('<Button-1>', handle_query)

# Search Results Listbox
search_results = Listbox(topFrame, width=80, height=30,
                         borderwidth=20, relief=FLAT)
search_results.grid(row=3, columnspan=2)
