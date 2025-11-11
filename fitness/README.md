# create_bigram.py

Quick reference for the bigram generator that populates `fitness/bigram_dict.json`.

## What It Does
- Scans text and counts consecutive character pairs (bigrams) while normalizing to lowercase.
- Treats capital letters as two-symbol sequences using `^` to capture case shifts (e.g., `a` followed by `B` becomes `a^` and `^b`).
- Writes the aggregated counts to JSON so latency models can use fresh frequency data.
- These are used in main.py. This is how you update the bigrams!

## Preparing Inputs
- **Corpus mode (default):** drop any `.txt` files you like into `fitness/corpus/` (books, articles, transcripts, etc.). Every `.txt` file in the directory is ingested.
- **Reddit mode:** download or `git clone https://github.com/linanqiu/reddit-dataset` and point `--directory` at its CSV dump folder (one post per row with the second column named `text`).

## Running The Script
```bash
uv run fitness/create_bigram.py \
  --directory fitness/corpus \
  --output-file fitness/bigram_dict.json

uv run fitness/create_bigram.py \
  --directory fitness/reddit_corpus \
  --reddit
```

Flags:
- `--directory /path/to/files` selects the source folder (defaults to `fitness/corpus`).
- `--reddit` switches to CSV parsing; omit it for plain-text parsing.
- `--output-file path.json` changes the JSON destination (defaults to `fitness/bigram_dict.json`).

After the run, the script prints the number of unique bigrams discovered and writes the JSON file you can commit alongside any corpus changes. This is then used by main.py to create a new keyboard.
