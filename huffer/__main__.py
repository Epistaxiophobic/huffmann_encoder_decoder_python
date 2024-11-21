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
        cfl.sort(key=lambda x: x.value if isinstance(x, Node) else x[1])
    return cfl[0]

def main():
    # Add command line arguments
    parser = argparse.ArgumentParser(description="A huffmann encoder decoder written in python")
    parser.add_argument("MDOE", type=str, help="the operation mode of the program, e for encode / d for decode")
    parser.add_argument("FILE", type=str, nargs="?", help="if FILE is - or no file is specified read standard input")
    args = parser.parse_args()

    data = ""

    if args.FILE is None or args.FILE == "-":
        data = stdin.read()
    else:
        # Check file validity
        if not exists(args.FILE):
            print(f"No such file or directory: {args.FILE}")
            quit()
        if not isfile(args.FILE):
            print(f"{args.FILE}: is not a file")
            quit()
        # Read file
        with open(args.FILE, "r") as fh:
            for line in fh:
                data += line
    # Build Huffmann tree    
    char_freq_dict = get_char_freq_dict(data)
    char_freq_lst = [(c, char_freq_dict[c]) for c in sorted(char_freq_dict.keys(), key=lambda x: char_freq_dict[x], reverse=True)]
    huff_tree = build_huffmann_tree(char_freq_lst)
    
if __name__ == "__main__":
    main()
