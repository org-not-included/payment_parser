import argparse
from helpers import parse_doc

if __name__ == '__main__':
    parser = argparse.ArgumentParser("payment_parser")
    parser.add_argument(
        "--file", help="The absolute path of the file to parse."
    )
    parser.add_argument(
        "--output_dir", help="The absolute folder path for saving the parse results.",
    )
    parser.add_argument(
        "--split_term", help="Word or phrase used to split file into chunks.",
    )
    parser.add_argument(
        "--verbose", help="Whether to enable extra logging.",
    )
    input_args = parser.parse_args()
    file = 'payment_parser/T140_sample.txt'
    output_dir = "payment_parser/output/"
    verbose = True
    split_term = "MASTERCARD WORLDWIDE"
    if input_args.file is not None:
        file = input_args.file
    if input_args.output_dir is not None:
        output_dir = input_args.output_dir
    if input_args.split_term is not None:
        output_dir = input_args.split_term
    if input_args.verbose is not None:
        verbose = (input_args.verbose in ("True", "true", "1"))

    print(f"File: {file}, Split Term: {split_term}, Output Dir: {output_dir}, Verbose: {verbose}")
    parse_doc(file, output_dir, split_term, verbose)