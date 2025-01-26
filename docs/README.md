# Local Demultiplexer

This repository provides tools for processing and demultiplexing FASTQ files based on index pairs and concatenating sequencing reads efficiently.

## Features

- Split large FASTQ files into smaller chunks for efficient processing.
- Extract reads from FASTQ files based on i7 and i5 index pairs.
- Concatenate and validate FASTQ files.
- Shell scripts for splitting and submitting jobs sequentially.

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/yourusername/local_demultiplexer.git
cd local_demultiplexer
pip install -r requirements.txt
```

## Usage

### Step 1: Split FASTQ Files

Split large `undetermined.fastq.R1.gz` and `undetermined.fastq.R2.gz` files into smaller FASTQ files for efficient processing.

```bash
bash scripts/split_fastq.sh input_folder output_folder
```

### Step 2: Demultiplex Reads

Submit jobs sequentially to demultiplex the reads using index pairs.

```bash
bash scripts/submit_sequential_log.sh job_list.txt
```

### Step 3: Concatenate and Validate FASTQ Files

Once reads are extracted, concatenate them separately for R1 and R2 using barcode-based grouping.

```bash
python local_demultiplexer/concatenate_fastq.py \
    --r1_dir R1_files/ \
    --r2_dir R2_files/ \
    --output_dir merged/ \
    --log_file process.log
```

## GitHub Actions Workflow

To automate the workflow using GitHub Actions, create a `.github/workflows/main.yml` file with the following content:

```yaml
name: Local Demultiplexer Workflow

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.8'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run tests
        run: |
          python -m unittest discover tests
```

## Project Structure

```
local_demultiplexer/
│-- local_demultiplexer/
│   │-- __init__.py
│   │-- extract_reads.py
│   │-- concatenate_fastq.py
│-- scripts/
│   │-- split_fastq.sh
│   │-- submit_sequential_log.sh
│-- tests/
│   │-- test_extract_reads.py
│   │-- test_concatenate_fastq.py
│   │-- test_data/
│       │-- test.fastq.gz
│       │-- index_pairs.txt
│-- docs/
│   │-- README.md
│-- .github/
│   │-- workflows/
│       │-- main.yml
│-- .gitignore
│-- setup.py
│-- requirements.txt
│-- LICENSE
```

## Contributions

Contributions are welcome! Please submit pull requests or open issues for suggestions and bug reports.

## Contact

For any inquiries, please contact [your email].

