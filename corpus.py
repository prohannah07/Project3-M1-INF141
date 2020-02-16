import json
import os
import index
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


def print_first_20_urls(query, doc_id_list, file_directory, output_file):
    len_ll = index.ll_len(doc_id_list)
    output_file.write("QUERY: " + query + "\n")
    output_file.write("NUMBER OF URLs RETRIEVED: " + str(len_ll) + "\n")
    output_file.write("FIRST 20 URLs:" + "\n")
    count = 0
    currentNode = doc_id_list.head
    if len_ll < 20:
        while(currentNode != None):
            docID = currentNode.data
            print(str(count + 1) + "\t" + "docID: " +
                  docID + "\t" + "URL: " + file_directory[docID])
            output_file.write(str(count + 1) + "\t" + "docID: " +
                              docID + "\t" + "URL: " + file_directory[docID] + "\n")
            count += 1
            currentNode = currentNode.next
        # for docID in doc_id_list:
        #     if count != len_ll:
        #         print(str(count + 1), file_directory[docID])
        #         # output_file.write(str(count + 1) + ": " + file_directory[docID])
        #         count += 1
        #     else:
        #         break
    else:
        while(count < 20):
            docID = currentNode.data
            print(str(count + 1) + "\t" + "docID: " +
                  docID + "\t" + "URL: " + file_directory[docID])
            output_file.write(str(count + 1) + "\t" + "docID: " +
                              docID + "\t" + "URL: " + file_directory[docID] + "\n")
            count += 1
            currentNode = currentNode.next
        # for docID in doc_id_list:
        #     if count != 20:
        #         print(str(count + 1), file_directory[docID])
        #         # output_file.write(str(count + 1) + ": " + file_directory[docID])
        #         count += 1
        #     else:
        #         break
