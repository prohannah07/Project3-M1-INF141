import sys


# Node class
class Node:

    # Function to initialize the node object
    def __init__(self, data):
        self.data = data  # Assign data
        self.next = None  # Initialize
        # next as null

# Linked List class


class LinkedList:

    # Function to initialize the Linked
    # List object
    def __init__(self):
        self.head = None


def build_index():
    pass


def index_size(index_dict):
    size = sys.getsizeof(index_dict)
    print("INDEX SIZE ON DISK: ", size, "bytes")
    return size
