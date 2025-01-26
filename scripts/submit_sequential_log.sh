#!/bin/bash

# Array range
START=1
END=16

# SLURM settings for initial job
JOB_NAME="split"
EMAIL="kaushalakhilesh@uams.edu"
NODELIST="n003"
NODES=1
NTASKS=1
TIME="240:00:00"

# File paths
INPUT_PREFIX="/home/kaushala/cutnatag/split_R2/Undetermined_S0_L001_R2_001_part"
INDEX_FILE="/home/kaushala/cutnatag/SampleSheet.index1reversed.txt"
OUTPUT_PREFIX="/scratch/genomics/cutnatag/demuxed_R2/part"
LOG_FILE="processing_log_R2.txt"

# Initialize the log file
echo "Processing log started at $(date)" > $LOG_FILE

# Loop through the range
PREV_JOB_ID=""
for PART in $(seq $START $END); do
    INPUT_FILE="${INPUT_PREFIX}${PART}.fastq.gz"
    OUTPUT_FILE="${OUTPUT_PREFIX}${PART}"

    # Log the details of the current task
    echo "Processing PART=${PART}" >> $LOG_FILE
    echo "Input file: ${INPUT_FILE}" >> $LOG_FILE
    echo "Index file: ${INDEX_FILE}" >> $LOG_FILE
    echo "Output file: ${OUTPUT_FILE}" >> $LOG_FILE
    echo "--------------------------" >> $LOG_FILE

    if [ -z "$PREV_JOB_ID" ]; then
        # Submit the first job without dependency
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

htseq_parser.bin -i ${INPUT_FILE} -ix ${INDEX_FILE} -o ${OUTPUT_FILE}
EOF
)
    else
        # Submit subsequent jobs with dependency
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

htseq_parser.bin -i ${INPUT_FILE} -ix ${INDEX_FILE} -o ${OUTPUT_FILE}
EOF
)
    fi

    # Update previous job ID
    PREV_JOB_ID=$JOB_ID
done

# Add completion timestamp to the log
echo "Processing log ended at $(date)" >> $LOG_FILE
