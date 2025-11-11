import json
from collections import defaultdict
import os
import argparse
import csv


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


def add_bigrams_from_text_string(text, bigram_dict):
    """Process a text string and add its bigrams to the dictionary"""
    for i in range(1, len(text)):
        last_letter = text[i-1]
        current_letter = text[i]

        if not _is_valid_letter(last_letter) or not _is_valid_letter(current_letter):
            continue
        if current_letter.isupper():
            bigram_dict["^" + current_letter.lower()] += 1
            bigram_dict[last_letter.lower() + "^"] += 1
        else:
            bigram_dict[last_letter.lower() + current_letter.lower()] += 1
    return bigram_dict


def add_bigrams_from_reddit_csv(csv_file_name, bigram_dict):
    """Parse a Reddit dataset CSV file and extract bigrams from the 'text' column"""
    try:
        with open(csv_file_name, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the first row (header)
            for row in reader:
                if len(row) > 1 and row[1]:
                    text = row[1]
                    add_bigrams_from_text_string(text, bigram_dict)
    except Exception as e:
        print(f"Error processing {csv_file_name}: {e}")
    
    return bigram_dict


def create_bigram_dict_from_reddit(directory_path):
    """Create bigram dictionary from Reddit dataset CSV files in a directory"""
    bigram_dict = defaultdict(lambda: 0)
    csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
    
    print(f"Found {len(csv_files)} CSV files in {directory_path}")
    
    for i, file in enumerate(csv_files, 1):
        file_path = os.path.join(directory_path, file)
        print(f"Processing {i}/{len(csv_files)}: {file}")
        add_bigrams_from_reddit_csv(file_path, bigram_dict)
    
    return bigram_dict


def create_bigram_dict_from_directory(directory_path):
    bigram_dict = defaultdict(lambda: 0)
    for file in os.listdir(directory_path):
        if file.endswith('.txt'):
            add_bigrams_from_txt_to_dict(os.path.join(directory_path, file), bigram_dict)
    return bigram_dict

def main():
    parser = argparse.ArgumentParser(description="Create bigram dictionary from directory")
    parser.add_argument('--directory', '-d', type=str, default='fitness/corpus', help="directory to create bigram dictionary from")
    parser.add_argument('--output-file', '-o', type=str, default='fitness/bigram_dict.json', help="output file to save bigram dictionary to")
    parser.add_argument('--reddit', '-r', action='store_true', help="parse Reddit dataset CSV files instead of txt files")
    args = parser.parse_args()
    
    if args.reddit:
        print("Parsing Reddit dataset CSV files...")
        bigram_dict = create_bigram_dict_from_reddit(args.directory)
    else:
        print("Parsing text files...")
        bigram_dict = create_bigram_dict_from_directory(args.directory)
    
    print(f"\nTotal unique bigrams: {len(bigram_dict)}")
    print(f"Saving to {args.output_file}...")
    
    with open(args.output_file, 'w') as f:
        json.dump(bigram_dict, f, indent=4)
    
    print("Done!")

if __name__ == "__main__":
    main()