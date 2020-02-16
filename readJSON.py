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
