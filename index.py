import sys


def build_index():
    pass


def index_size(index_dict):
    size = sys.getsizeof(index_dict)
    print("INDEX SIZE ON DISK: ", size, "bytes")
    return size
