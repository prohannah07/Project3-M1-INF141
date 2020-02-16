import json
import os
# import sys

# if __name__ == "__main__":
#     corpus = sys.argv[1]
#     corpus_json = os.path.join(corpus, "bookkeeping.json")

#     with open(corpus_json, 'r', encoding='utf8') as f:
#         file_directory = json.load(f)

#     print(file_directory["0/1"])


def json_to_dict(corpus_path):
    corpus_json = os.path.join(corpus_path, "bookkeeping.json")

    with open(corpus_json, 'r', encoding='utf8') as f:
        file_directory = json.load(f)

    return file_directory


def print_first_20_urls(doc_id_list, file_directory, output_file):
    count = 0
    for docID in doc_id_list:
        if count != 20:
            print(str(count + 1), file_directory[docID])
            # output_file.write(str(count + 1) + ": " + file_directory[docID])
            count += 1
        else:
            break
