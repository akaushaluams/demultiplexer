import os
import gzip
import argparse
import logging

class FastqConcatenator:
    def __init__(self, r1_dir, r2_dir, output_dir, log_file):
        self.r1_dir = r1_dir
        self.r2_dir = r2_dir
        self.output_dir = output_dir
        logging.basicConfig(filename=log_file, level=logging.DEBUG, 
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def concatenate_files(self):
        os.makedirs(self.output_dir, exist_ok=True)
        for prefix in os.listdir(self.r1_dir):
            r1_file = os.path.join(self.r1_dir, prefix)
            r2_file = os.path.join(self.r2_dir, prefix.replace('R1', 'R2'))
            output_file = os.path.join(self.output_dir, prefix.replace('R1', 'merged'))

            with gzip.open(output_file, 'wb') as out_f:
                for file_path in [r1_file, r2_file]:
                    with gzip.open(file_path, 'rb') as in_f:
                        out_f.writelines(in_f)
            logging.info(f"Concatenated {r1_file} and {r2_file} into {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Concatenate and validate FASTQ files.")
    parser.add_argument("--r1_dir", required=True)
    parser.add_argument("--r2_dir", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--log_file", required=True)
    args = parser.parse_args()
    concatenator = FastqConcatenator(args.r1_dir, args.r2_dir, args.output_dir, args.log_file)
    concatenator.concatenate_files()

if __name__ == "__main__":
    main()
