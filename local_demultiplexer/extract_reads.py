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
        """
        Attempt to create a temporary directory within the output directory.
        If that fails, use the default system temp directory.
        """
        temp_dir = os.path.join(self.output_dir, "temp_index_reads")
        try:
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            return temp_dir
        except Exception as e:
            print(f"Warning: Could not create temp directory in output directory. Using system temp directory instead. Error: {e}")
            return tempfile.mkdtemp()

    def _read_index_pairs(self):
        """
        Read i7 and i5 indices from a file and return a list of tuples (i7, i5).
        The file should have two columns: i7_index and i5_index, tab-separated.
        """
        index_pairs = []
        if not os.path.isfile(self.index_pairs_file):
            sys.exit(f"Error: Index pairs file '{self.index_pairs_file}' not found.")

        with open(self.index_pairs_file, 'r') as file:
            for line_num, line in enumerate(file, start=1):
                if not line.strip():
                    continue

                parts = line.strip().split("\t")
                if len(parts) != 2:
                    print(f"Warning: Line {line_num} in '{self.index_pairs_file}' does not have exactly two columns. Skipping this line.")
                    continue

                i7, i5 = parts
                index_pairs.append((i7, i5))
        return index_pairs

    def extract_reads(self):
        """
        Extract reads based on matching the 10th field in headers with the given index pairs.
        Write each read as a separate FASTQ file in individual temp folders.
        """
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
            read_count = 0

            for read in reader:
                header_parts = read.name.split(":")
                if len(header_parts) >= 10:
                    index_field = header_parts[9]

                    for i7, i5 in self.index_pairs:
                        if i7 in index_field and i5 in index_field:
                            temp_file_path = os.path.join(temp_dirs[(i7, i5)], f"read_{read_count}.fastq")
                            with open(temp_file_path, 'w') as temp_file:
                                # Ensure sequence and quality strings are properly decoded if in bytes
                                sequence_string = read.seq if isinstance(read.seq, str) else read.seq.decode()
                                quality_string = ''.join(chr(q + 33) for q in read.qual)
                                temp_file.write(f"@{read.name}\n{sequence_string}\n+\n{quality_string}\n")
                            read_count += 1

        for (i7, i5), temp_dir_path in temp_dirs.items():
            output_file = os.path.join(self.output_dir, f"{i7}_{i5}_reads.fastq")
            with open(output_file, 'wb') as outfile:
                for temp_file in sorted(os.listdir(temp_dir_path)):
                    temp_file_path = os.path.join(temp_dir_path, temp_file)
                    with open(temp_file_path, 'rb') as infile:
                        shutil.copyfileobj(infile, outfile)

            # Compress the output FASTQ file
            compressed_output_file = f"{output_file}.gz"
            with open(output_file, 'rb') as f_in, gzip.open(compressed_output_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

            # Remove the uncompressed file
            os.remove(output_file)

        shutil.rmtree(self.temp_dir)

def main():
    parser = argparse.ArgumentParser(description="Extract reads from a FASTQ file based on i7 and i5 index pairs.")
    parser.add_argument("-i", "--input_fastq", required=True, help="Input FASTQ file (can be gzipped).")
    parser.add_argument("-ix", "--index_pairs", required=True, help="File containing i7 and i5 index pairs (comma-separated).")
    parser.add_argument("-o", "--output_dir", required=True, help="Output directory to store extracted reads.")

    args = parser.parse_args()

    extractor = FastqExtractor(args.input_fastq, args.index_pairs, args.output_dir)
    extractor.extract_reads()

if __name__ == "__main__":
    main()
