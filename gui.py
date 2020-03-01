from tkinter import *
from functools import partial
import json
import os
from bs4 import BeautifulSoup

corpus_path = ""
index = {}
file_directory = {}


def json_to_dict():
    global file_directory
    corpus_json = os.path.join(corpus_path, "bookkeeping.json")

    with open(corpus_json, 'r', encoding='utf8') as f:
        file_directory = json.load(f)


def index_to_dict(index_path):
    global index

    with open(index_path, 'r', encoding='utf8') as f:
        index = json.load(f)


def handle_query(entry, no_match_label):
    query = entry.get().lower()

    if query == "":
        print("TYPE SOMETHING!")
    elif query not in index:
        noMatchLabel.grid()
        print("No Matches")
    else:
        no_match_label.grid_remove()
        # delete_frame_labels()
        search_results.delete(0, END)

        print(query, index[query])
        for posting in index[query]:
            print(file_directory[posting])
        make_labels_for_urls(index[query])


def make_labels_for_urls(index_query):
    title_row = 0
    url_row = 1
    space_row = 2
    for posting in index_query:
        title = get_url_title(posting)
        get_url_description(posting)
        # Label(bottomFrame, text="title: " + title).grid(row=title_row)
        # Label(bottomFrame, text=file_directory[posting]).grid(row=url_row)
        search_results.insert(title_row, title)
        search_results.insert(url_row, file_directory[posting])
        search_results.insert(
            space_row, "--------------------------------------------------------------------------------")
        title_row += 3
        url_row += 3
        space_row += 3


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
    text = soup.get_text().split('\n')
    if len(text) == 0:
        print("NO DESCRIPTION")
        return "NO DESCRIPTION"
    else:
        print(' '.join(text)[0:100])
        return ' '.join(text)[0:100]


# def delete_frame_labels():
#     labels = []
#     for label in bottomFrame.children.values():
#         labels.append(label)
#     for label in labels:
#         label.destroy()


root = Tk()
root.title("Rey and Hannah's Search Engine")

topFrame = Frame()
topFrame.pack()
# bottomFrame = Frame()
# bottomFrame.pack(side=BOTTOM)

theLabel = Label(topFrame, text="Rey and Hannah's Search Engine!")
theLabel.grid(row=0, columnspan=2)

noMatchLabel = Label(topFrame, text="No Matches", fg="red")
noMatchLabel.grid(row=2, columnspan=2)
noMatchLabel.grid_remove()

search_entry = Entry(topFrame, width=50, borderwidth=7,
                     relief=FLAT, highlightcolor="purple", highlightbackground="purple")
search_entry.grid(row=1, column=0, sticky=E)

handle_query_with_arg = partial(handle_query, search_entry, noMatchLabel)
search_button = Button(topFrame, text="Search",
                       command=handle_query_with_arg, height=2, width=10)
search_button.grid(row=1, column=1, sticky=W)

search_results = Listbox(topFrame, width=80, height=50,
                         borderwidth=20, relief=FLAT)
search_results.grid(row=3, columnspan=2)

# root.maxsize(1000, 500)
# root.minsize(1000, 500)


# root = Tk()

# topframe = Frame(root)
# entry = Entry(topframe)
# entry.pack()

# button = Button(topframe, text="Search")
# button.pack()

# topframe.pack(side=TOP)

# bottomframe = Frame(root)

# scroll = Scrollbar(bottomframe)
# scroll.pack(side=RIGHT, fill=Y)
# answer = Text(bottomframe, width=70, height=30, yscrollcommand=scroll.set)
# scroll.config(command=answer.yview)
# answer.pack()

# bottomframe.pack()
