import json
from collections import defaultdict
import os
import argparse


def _is_valid_letter(letter):
    return letter.isalpha() or letter == "^" or letter == " "

def add_bigrams_from_txt_to_dict(txt_file_name, bigram_dict):

    with open(txt_file_name, 'r') as f:
        text = f.read()

    for i in range(1,len(text)):
        last_letter = text[i-1]
        current_letter = text[i]

        if not _is_valid_letter(last_letter) or not _is_valid_letter(current_letter):
            continue
        if current_letter.isupper():
            
            bigram_dict["^" + current_letter.lower()] += 1
            bigram_dict[last_letter.lower() + "^"] += 1
        else:
            bigram_dict[last_letter.lower() + current_letter.lower()] += 1
        last_letter = current_letter
    return bigram_dict


def create_bigram_dict_from_directory(directory_path):
    bigram_dict = defaultdict(lambda: 0)
    for file in os.listdir(directory_path):
        if file.endswith('.txt'):
            add_bigrams_from_txt_to_dict(os.path.join(directory_path, file), bigram_dict)
    return bigram_dict

def main():
    parser = argparse.ArgumentParser(description="Create bigram dictionary from directory")
    parser.add_argument('--directory', '-d', type=str, default='corpus', help="directory to create bigram dictionary from")
    parser.add_argument('--output-file', '-o', type=str, default='bigram_dict.json', help="output file to save bigram dictionary to")
    args = parser.parse_args()
    bigram_dict = create_bigram_dict_from_directory(args.directory)
    with open(args.output_file, 'w') as f:
        json.dump(bigram_dict, f, indent=4)

if __name__ == "__main__":
    main()
