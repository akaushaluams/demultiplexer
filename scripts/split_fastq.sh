#!/bin/bash

# Check for required arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input.fastq.gz> <number_of_parts>"
    exit 1
fi

# Arguments
INPUT_FILE=$1
NUM_PARTS=$2

# Ensure input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File $INPUT_FILE not found."
    exit 1
fi

# Calculate number of reads per chunk
TOTAL_LINES=$(zcat "$INPUT_FILE" | wc -l)
if (( TOTAL_LINES % 4 != 0 )); then
    echo "Error: FASTQ file is not properly formatted (line count not divisible by 4)."
    exit 1
fi

TOTAL_READS=$(( TOTAL_LINES / 4 ))
READS_PER_CHUNK=$(( TOTAL_READS / NUM_PARTS ))

if (( READS_PER_CHUNK == 0 )); then
    echo "Error: Too many parts requested for the size of the input file."
    exit 1
fi

# Split the file
echo "Splitting $INPUT_FILE into $NUM_PARTS parts..."
zcat "$INPUT_FILE" | split -l $(( READS_PER_CHUNK * 4 )) - split_

# Recompress using parallel
echo "Recompressing split files..."
ls split_* | parallel gzip

# Rename files sequentially
echo "Renaming output files..."
COUNT=1
for FILE in split_*.gz; do
    mv "$FILE" "$(basename "$INPUT_FILE" .fastq.gz)_part${COUNT}.fastq.gz"
    COUNT=$((COUNT + 1))
done

echo "Done. Files saved as $(basename "$INPUT_FILE" .fastq.gz)_part[1-$NUM_PARTS].fastq.gz"
