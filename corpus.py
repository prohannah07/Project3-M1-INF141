import json
import os
import index
from math import sqrt
from math import log10

def json_to_dict(corpus_path):
    corpus_json = os.path.join(corpus_path, "bookkeeping.json")

    with open(corpus_json, 'r', encoding='utf8') as f:
        file_directory = json.load(f)

    return file_directory


def print_first_20_urls(query, doc_id_list, file_directory, output_file):
    len_ll = doc_id_list.len
    output_file.write("QUERY: " + query + "\n")
    output_file.write("NUMBER OF URLs RETRIEVED: " + str(len_ll) + "\n")
    output_file.write("FIRST 20 URLs:" + "\n")
    count = 0
    currentNode = doc_id_list.head
    if len_ll < 20:
        while(currentNode != None):
            docID = currentNode.docID
            print(str(count + 1) + "\t" + "docID: " +
                  docID + "\t" + "URL: " + file_directory[docID])
            output_file.write(str(count + 1) + "\t" + "docID: " +
                              docID + "\t" + "URL: " + file_directory[docID] + "\n")
            count += 1
            currentNode = currentNode.next
    else:
        while(count < 20):
            docID = currentNode.docID
            print(str(count + 1) + "\t" + "docID: " +
                  docID + "\t" + "URL: " + file_directory[docID])
            output_file.write(str(count + 1) + "\t" + "docID: " +
                              docID + "\t" + "URL: " + file_directory[docID] + "\n")
            count += 1
            currentNode = currentNode.next


def print_ranked_results(query_search, file_directory, output_file):
    output_file.write("NUMBER OF URLs RETRIEVED: " + str(len(query_search)) + "\n")
    output_file.write("FIRST 20 URLs:" + "\n")
    count = 0
    docID_results = []
    ranked = sorted( list(query_search.items()) , key =  lambda x:x[1]["document_score"], reverse=True)
    if len(ranked) < 20:
        for docID in ranked:
            docID_results.append(docID[0])
            print(str(count + 1) + "\t" + "docID: " +
                docID[0] + "\t" + "score: " + str(docID[1]["document_score"]) + "\t" + "URL: " + file_directory[docID[0]])
            output_file.write(str(count + 1) + "\t" + "docID: " +
                            docID[0] + "\t" + "score: " + str(docID[1]["document_score"]) + "\t" + "URL: " + file_directory[docID[0]] + "\n")
            count += 1
    else:
        for docID in ranked:
            if count < 20:
                docID_results.append(docID[0])
                print(str(count + 1) + "\t" + "docID: " +
                    docID[0] + "\t" + "score: " + str(docID[1]["document_score"]) + "\t" + "URL: " + file_directory[docID[0]])
                output_file.write(str(count + 1) + "\t" + "docID: " +
                                docID[0] + "\t" + "score: " + str(docID[1]["document_score"]) + "\t" + "URL: " + file_directory[docID[0]] + "\n")
                count += 1
            else:
                break
    return docID_results


def retrieve_corpus_data(qtoken, qtoken_freq, query_terms, query_search, index_file):
    for line in index_file:
        token_posting_pair = line.split("|")
        token = token_posting_pair[0:3]
        postings = token_posting_pair[3:]
        if(token[0] == qtoken):
            for document in postings:
                document_info = document.split(";")
                docID = document_info[0]
                if qtoken not in query_terms:
                    tf_idf = (1 + log10(qtoken_freq))*float(token[2])
                    query_terms[qtoken] = {"weight":tf_idf, "normal":0}
                    query_terms["length_norm"] += tf_idf * tf_idf
                if docID not in query_search:
                    term = qtoken
                    tf_idf = float(document_info[1])
                    query_search[docID] = {}
                    query_search[docID]["length_norm"] = tf_idf * tf_idf
                    query_search[docID]["document_score"] = 0
                    query_search[docID][term] = {"weight":tf_idf, "normal":0}
                elif docID in query_search:
                    term = qtoken
                    tf_idf = float(document_info[1])
                    query_search[docID]["length_norm"] += tf_idf * tf_idf
                    query_search[docID][term] = {"weight":tf_idf, "normal":0}


# def normalize_terms(query_terms, query_search):
#     query_terms['length_norm'] = sqrt(query_terms['length_norm'])
#     query_terms_normalizer = query_terms['length_norm']
#     for term in query_terms:
#         if term != "length_norm" and term != "document_score":
#             # Normalization of each query term in query
#             query_terms[term]["normal"] = query_terms[term]["weight"] / query_terms_normalizer
#     for docID in query_search:
#         query_search[docID]["length_norm"] = sqrt(query_search[docID]["length_norm"])
#         query_search_normalizer = query_search[docID]['length_norm']
#         for term in query_search[docID]:
#             if term != "length_norm" and term != "document_score":
#                 # Normalization of each term in document
#                 query_search[docID][term]["normal"] = query_search[docID][term]["weight"] / query_search_normalizer
#                 # term normalization * query term normalization = document term dot product
#                 # document score += document term dot product
#                 query_search[docID]["document_score"] += query_search[docID][term]["normal"] * query_terms[term]["normal"]


# def normalize_terms(query_terms, query_search, reference_file):
#     query_terms['length_norm'] = sqrt(query_terms['length_norm'])
#     query_terms_normalizer = query_terms['length_norm']
#     for term in query_terms:
#         if term != "length_norm" and term != "document_score":
#             # Normalization of each query term in query
#             query_terms[term]["normal"] = query_terms[term]["weight"] / query_terms_normalizer
#     for docID in query_search:
#         ref_file = open(reference_file,'r')
#         for line in ref_file:
#             document_token_pair = line.split("|")
#             document = document_token_pair[0]
#             tokens = document_token_pair[1:]
#             if document == docID:
#                 for token in tokens:
#                     token = token.split(";")
#                     if token[0] not in query_search[docID]:
#                         term = token[0]
#                         query_search[docID][term] = {"weight":float(token[1]), "normal":0}
#                         tf_idf = query_search[docID][term]["weight"]
#                         query_search[docID]["length_norm"] += tf_idf * tf_idf
#         ref_file.close()
#     for docID in query_search:
#         query_search[docID]["length_norm"] = sqrt(query_search[docID]["length_norm"])
#         query_search_normalizer = query_search[docID]['length_norm']
#         for term in query_search[docID]:
#             if term != "length_norm" and term in query_terms:
#                 # Normalization of each term in document
#                 query_search[docID][term]["normal"] = query_search[docID][term]["weight"] / query_search_normalizer
#                 # term normalization * query term normalization = document term dot product
#                 # document score += document term dot product
#                 query_search[docID]["document_score"] += query_search[docID][term]["normal"] * query_terms[term]["normal"]


def normalize_terms(query_terms, query_search, reference_file):
    query_terms['length_norm'] = sqrt(query_terms['length_norm'])
    query_terms_normalizer = query_terms['length_norm']
    reference_documents = {}
    for term in query_terms:
        if term != "length_norm" and term != "document_score":
            # Normalization of each query term in query
            query_terms[term]["normal"] = query_terms[term]["weight"] / query_terms_normalizer
    ref_file = open(reference_file,'r')
    for line in ref_file:
        document_token_pair = line.split("|")
        document = document_token_pair[0]
        token_count = document_token_pair[1]
        if document in query_search:
            query_search[document]["length_norm"] += int(token_count) - len(query_terms)
    ref_file.close()
    for docID in query_search:
        query_search[docID]["length_norm"] = sqrt(query_search[docID]["length_norm"])
        query_search_normalizer = query_search[docID]['length_norm']
        for term in query_search[docID]:
            if term != "length_norm" and term != "document_score":
                # Normalization of each term in document
                query_search[docID][term]["normal"] = query_search[docID][term]["weight"] / query_search_normalizer
                # term normalization * query term normalization = document term dot product
                # document score += document term dot product
                query_search[docID]["document_score"] += query_search[docID][term]["normal"] * query_terms[term]["normal"]


def compute_dot_product(query_terms, query_search):
    pass

def compute_score(query_terms, query_search):
    pass


