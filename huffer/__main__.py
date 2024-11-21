import argparse
from os.path import exists, isfile
from sys import stdin

def get_char_freq_dict(s):
    res = {}
    for c in s:
        res[c] = res.get(c, 0) + 1
    return res

class Node:
    def __init__(self, right, left, value):
        self.right = right
        self.left = left
        self.value = value

def build_huffmann_tree(char_freq_lst):
    cfl = char_freq_lst[:]
    while len(cfl) > 1:
        value = 0
        right = cfl.pop()
        value += right.value if isinstance(right, Node) else right[1]
        left = cfl.pop()
        value += left.value if isinstance(left, Node) else left[1]
        node = Node(right, left, value)
        cfl.append(node)
        cfl.sort(key=lambda x: x.value if isinstance(x, Node) else x[1], reverse=True)
    return cfl[0]

def create_encoding_table(tree):
    def traverse_the_tree(node, table, encoding):
        if not node:
            return
        if not isinstance(node, Node):
            table[node[0]] = encoding
            return
        traverse_the_tree(node.right, table, encoding + "1")
        traverse_the_tree(node.left, table, encoding + "0")

    table = {}
    traverse_the_tree(tree, table, "")
    return table

def encode(path):
    data = ""

    if path is None or path == "-":
        data = stdin.read()
    else:
        # Check file validity
        if not exists(path):
            print(f"No such file or directory: {path}")
            quit()
        if not isfile(path):
            print(f"{path}: is not a file")
            quit()
        # Read file
        with open(path, "r") as fh:
            for line in fh:
                data += line
    # Build Huffmann tree    
    char_freq_dict = get_char_freq_dict(data)
    char_freq_lst = [(c, char_freq_dict[c]) for c in sorted(char_freq_dict.keys(), key=lambda x: char_freq_dict[x], reverse=True)]
    huff_tree = build_huffmann_tree(char_freq_lst)
    # Create encoding table     
    char_encoding_lst = create_encoding_table(huff_tree)
    # Encode the data
    res = ""
    for c in data:
        res += char_encoding_lst[c]
    # Get file name
    out_name = ""
    while len(out_name) == 0:
        out_name = input("type a name for the output file name: ")
    
    # Create header
    header = f"{len(char_freq_lst)}"
    for x in char_freq_lst:
        header += f"{x[0]}\0{x[1]}\0"

    with open(out_name, "wb") as fh:
        fh.write(bytes(header, encoding="utf-8"))
        i = 0
        while i < len(res):
            curr = res[i:i + 8]
            while len(curr) < 8:
                curr += "0"
            i += 8
            fh.write(int(curr, 2).to_bytes(1, byteorder="big"))

def main():
    # Add command line arguments
    parser = argparse.ArgumentParser(description="A huffmann encoder decoder written in python")
    parser.add_argument("MODE", type=str, help="the operation mode of the program, e for encode / d for decode")
    parser.add_argument("FILE", type=str, nargs="?", help="if FILE is - or no file is specified read standard input")
    args = parser.parse_args()
    
    if args.MODE == "e":
        encode(args.FILE)
    else:
        print(f"Invalid MODE: {args.MODE}")

if __name__ == "__main__":
    main()
