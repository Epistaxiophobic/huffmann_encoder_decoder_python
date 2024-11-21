import argparse
from os.path import exists, isfile
from sys import stdin

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
        if not exists(args.FILE):
            print(f"No such file or directory: {args.FILE}")
            quit()
        if not isfile(args.FILE):
            print(f"{args.FILE}: is not a file")
            quit()
        with open(args.FILE, "r") as fh:
            for line in fh:
                data += line

if __name__ == "__main__":
    main()
