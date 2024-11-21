import argparse

def main():
    # Add command line arguments
    parser = argparse.ArgumentParser(description="A huffmann encoder decoder written in python")
    parser.add_argument("MDOE", type=str, help="the operation mode of the program, e for encode / d for decode")
    parser.add_argument("FILE", type=str, nargs="?", help="if FILE is - or no file is specified read standard input")
    args = parser.parse_args()

if __name__ == "__main__":
    main()
