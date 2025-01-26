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
bash scripts/split_fastq.sh undetermined...R1.fastq.gz 15
```

### Step 2: Demultiplex Reads

Submit jobs sequentially to demultiplex the reads using index pairs.

```bash
bash scripts/submit_sequential_log.sh 1 16 \
    /path/to/input_prefix \
    /path/to/index_file.txt \
    /path/to/output_prefix \
    process_log.txt
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
│-- docs/
│   │-- README.md
│-- .gitignore
│-- setup.py
│-- requirements.txt
│-- LICENSE
```

## .gitignore

```

```

## Setup.py

```python
from setuptools import setup, find_packages

setup(
    name='local_demultiplexer',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'HTSeq',
        'gzip'
    ],
    entry_points={
        'console_scripts': [
            'extract_reads=local_demultiplexer.extract_reads:main',
            'concatenate_fastq=local_demultiplexer.concatenate_fastq:main'
        ]
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A package for demultiplexing and processing FASTQ files.',
    license='MIT',
)
```

## Requirements.txt

```
HTSeq
gzip
```

## Tests

### test_concatenate_fastq.py

```python
import unittest
from local_demultiplexer.concatenate_fastq import FastqConcatenator

class TestFastqConcatenator(unittest.TestCase):
    def test_concatenation(self):
        concatenator = FastqConcatenator("test_R1", "test_R2", "output", "test.log")
        self.assertTrue(hasattr(concatenator, 'concatenate_files'))

if __name__ == '__main__':
    unittest.main()
```

### test_extract_reads.py

```python
import unittest
from local_demultiplexer.extract_reads import FastqExtractor

class TestFastqExtractor(unittest.TestCase):
    def test_extraction(self):
        extractor = FastqExtractor("test.fastq.gz", "index_pairs.txt", "output")
        self.assertTrue(hasattr(extractor, 'extract_reads'))

if __name__ == '__main__':
    unittest.main()
```

## License

```
MIT License

Copyright (c) [2025] [Akhilesh Kaushal]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

## Contributions

Contributions are welcome! Please submit pull requests or open issues for suggestions and bug reports.

## Contact

For any inquiries, please contact [akhileshkaushal@gmail.com].

