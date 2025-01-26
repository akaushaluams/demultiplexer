#!/bin/bash

# Parse arguments
START=$1
END=$2
INPUT_PREFIX=$3
INDEX_FILE=$4
OUTPUT_PREFIX=$5
LOG_FILE=$6

# SLURM settings
JOB_NAME="split"
EMAIL="your.email@example.com"
NODELIST="n003"
NODES=1
NTASKS=1
TIME="240:00:00"

# Initialize the log file
echo "Processing log started at $(date)" > $LOG_FILE

# Loop through the range
PREV_JOB_ID=""
for PART in $(seq $START $END); do
    INPUT_FILE="${INPUT_PREFIX}${PART}.fastq.gz"
    OUTPUT_FILE="${OUTPUT_PREFIX}${PART}"

    echo "Processing PART=${PART}" >> $LOG_FILE
    echo "Input file: ${INPUT_FILE}" >> $LOG_FILE
    echo "Index file: ${INDEX_FILE}" >> $LOG_FILE
    echo "Output file: ${OUTPUT_FILE}" >> $LOG_FILE
    echo "--------------------------" >> $LOG_FILE

    if [ -z "$PREV_JOB_ID" ]; then
        JOB_ID=$(sbatch <<EOF | awk '{print $4}'
#!/bin/bash
#SBATCH --job-name=${JOB_NAME}${PART}
#SBATCH --mail-user=${EMAIL}
#SBATCH --nodelist=${NODELIST}
#SBATCH --nodes=${NODES}
#SBATCH --ntasks=${NTASKS}
#SBATCH --time=${TIME}
#SBATCH -o split${PART}.out
#SBATCH -e split${PART}.err

date; hostname; pwd
echo "Processing input file: ${INPUT_FILE}" >> $LOG_FILE
echo "Using index file: ${INDEX_FILE}" >> $LOG_FILE
echo "Generating output file: ${OUTPUT_FILE}" >> $LOG_FILE

python extract_reads.py -i ${INPUT_FILE} -ix ${INDEX_FILE} -o ${OUTPUT_FILE}
EOF
)
    else
        JOB_ID=$(sbatch --dependency=afterok:${PREV_JOB_ID} <<EOF | awk '{print $4}'
#!/bin/bash
#SBATCH --job-name=${JOB_NAME}${PART}
#SBATCH --mail-user=${EMAIL}
#SBATCH --nodelist=${NODELIST}
#SBATCH --nodes=${NODES}
#SBATCH --ntasks=${NTASKS}
#SBATCH --time=${TIME}
#SBATCH -o split${PART}.out
#SBATCH -e split${PART}.err

date; hostname; pwd
echo "Processing input file: ${INPUT_FILE}" >> $LOG_FILE
echo "Using index file: ${INDEX_FILE}" >> $LOG_FILE
echo "Generating output file: ${OUTPUT_FILE}" >> $LOG_FILE

python extract_reads.py -i ${INPUT_FILE} -ix ${INDEX_FILE} -o ${OUTPUT_FILE}
EOF
)
    fi

    PREV_JOB_ID=$JOB_ID
done

echo "Processing log ended at $(date)" >> $LOG_FILE
