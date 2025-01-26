import argparse
import gzip
import os
import shutil
import sys
import tempfile
from HTSeq import FastqReader

class FastqExtractor:
    def __init__(self, input_fastq, index_pairs_file, output_dir):
        self.input_fastq = input_fastq
        self.index_pairs_file = index_pairs_file
        self.output_dir = output_dir
        self.temp_dir = self._create_temp_dir()
        self.index_pairs = self._read_index_pairs()

    def _create_temp_dir(self):
        temp_dir = os.path.join(self.output_dir, "temp_index_reads")
        try:
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            return temp_dir
        except Exception as e:
            print(f"Warning: Could not create temp directory in output directory. Using system temp directory instead. Error: {e}")
            return tempfile.mkdtemp()

    def _read_index_pairs(self):
        index_pairs = []
        if not os.path.isfile(self.index_pairs_file):
            sys.exit(f"Error: Index pairs file '{self.index_pairs_file}' not found.")

        with open(self.index_pairs_file, 'r') as file:
            for line in file:
                parts = line.strip().split("\t")
                if len(parts) == 2:
                    i7, i5 = parts
                    index_pairs.append((i7, i5))
        return index_pairs

    def extract_reads(self):
        temp_dirs = {}
        for i7, i5 in self.index_pairs:
            temp_dir_path = os.path.join(self.temp_dir, f"{i7}_{i5}")
            if not os.path.exists(temp_dir_path):
                os.makedirs(temp_dir_path)
            temp_dirs[(i7, i5)] = temp_dir_path

        if self.input_fastq.endswith(".gz"):
            open_func = lambda f: gzip.open(f, 'rt')
        else:
            open_func = lambda f: open(f, 'r')

        with open_func(self.input_fastq) as fastq_file:
            reader = FastqReader(fastq_file)
            for read in reader:
                header_parts = read.name.split(":")
                if len(header_parts) >= 10:
                    index_field = header_parts[9]
                    for i7, i5 in self.index_pairs:
                        if i7 in index_field and i5 in index_field:
                            temp_file_path = os.path.join(temp_dirs[(i7, i5)], "reads.fastq")
                            with open(temp_file_path, 'a') as temp_file:
                                temp_file.write(f"@{read.name}\n{read.seq}\n+\n{''.join(chr(q + 33) for q in read.qual)}\n")

def main():
    parser = argparse.ArgumentParser(description="Extract reads from FASTQ file based on index pairs.")
    parser.add_argument("-i", "--input_fastq", required=True)
    parser.add_argument("-ix", "--index_pairs", required=True)
    parser.add_argument("-o", "--output_dir", required=True)
    args = parser.parse_args()
    extractor = FastqExtractor(args.input_fastq, args.index_pairs, args.output_dir)
    extractor.extract_reads()

if __name__ == "__main__":
    main()
