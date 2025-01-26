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

    def get_file_groups(self, directory):
        """Group files based on their prefix."""
        file_groups = {}
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.fastq.gz'):
                    prefix = '_'.join(file.split('_')[:2])  # Extract prefix
                    if prefix not in file_groups:
                        file_groups[prefix] = []
                    file_groups[prefix].append(os.path.join(root, file))
        return file_groups

    def calculate_total_lines(self, files):
        """Calculate the total number of lines in a list of files."""
        total_lines = 0
        for file in files:
            try:
                with gzip.open(file, 'rt') as f:
                    for _ in f:
                        total_lines += 1
            except (gzip.BadGzipFile, EOFError) as e:
                logging.error(f"Error reading file {file}: {e}. Deleting corrupted file.")
                os.remove(file)
                raise
        return total_lines

    def calculate_output_lines(self, file):
        """Calculate the number of lines in an existing output file."""
        total_lines = 0
        try:
            with gzip.open(file, 'rt') as f:
                for _ in f:
                    total_lines += 1
        except (gzip.BadGzipFile, EOFError) as e:
            logging.error(f"Error reading output file {file}: {e}. Deleting corrupted file.")
            os.remove(file)
            raise
        return total_lines

    def concatenate_files(self, file_group, output_file):
        """Concatenate files in a group into a single output file."""
        for attempt in range(2):
            try:
                with gzip.open(output_file, 'wb') as out_f:
                    for file_path in sorted(file_group):
                        with gzip.open(file_path, 'rb') as in_f:
                            out_f.writelines(in_f)
                logging.info(f"Successfully concatenated files into {output_file}.")
                return
            except (gzip.BadGzipFile, EOFError) as e:
                logging.error(f"Error during concatenation attempt {attempt + 1} for {output_file}: {e}")
                if attempt == 1:
                    logging.error(f"Failed to concatenate after multiple attempts: {output_file}. Skipping.")
                    return

    def process(self):
        """Process R1 and R2 directories to create concatenated files."""
        os.makedirs(self.output_dir, exist_ok=True)

        # Process R1 files
        r1_groups = self.get_file_groups(self.r1_dir)
        for prefix, files in r1_groups.items():
            output_file = os.path.join(self.output_dir, f"{prefix}_R1.fastq.gz")
            try:
                total_lines = self.calculate_total_lines(files)

                if os.path.exists(output_file):
                    output_lines = self.calculate_output_lines(output_file)
                    if output_lines == total_lines:
                        logging.info(f"Skipping {output_file}: already exists and matches total lines.")
                        continue

                logging.info(f"Concatenating R1 files for {prefix} into {output_file}")
                self.concatenate_files(files, output_file)
            except Exception as e:
                logging.error(f"Failed to process R1 group {prefix}: {e}")

        # Process R2 files
        r2_groups = self.get_file_groups(self.r2_dir)
        for prefix, files in r2_groups.items():
            output_file = os.path.join(self.output_dir, f"{prefix}_R2.fastq.gz")
            try:
                total_lines = self.calculate_total_lines(files)

                if os.path.exists(output_file):
                    output_lines = self.calculate_output_lines(output_file)
                    if output_lines == total_lines:
                        logging.info(f"Skipping {output_file}: already exists and matches total lines.")
                        continue

                logging.info(f"Concatenating R2 files for {prefix} into {output_file}")
                self.concatenate_files(files, output_file)
            except Exception as e:
                logging.error(f"Failed to process R2 group {prefix}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Concatenate and Validate FASTQ Files by Line Count.")
    parser.add_argument("--r1_dir", required=True, help="Input directory for R1 files.")
    parser.add_argument("--r2_dir", required=True, help="Input directory for R2 files.")
    parser.add_argument("--output_dir", required=True, help="Output directory for concatenated files.")
    parser.add_argument("--log_file", required=True, help="Path to the log file.")

    args = parser.parse_args()

    concatenator = FastqConcatenator(args.r1_dir, args.r2_dir, args.output_dir, args.log_file)
    concatenator.process()
