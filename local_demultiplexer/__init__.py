"""
Local Demultiplexer Package

This package provides tools for processing and demultiplexing FASTQ files based on index pairs 
and concatenating sequencing reads efficiently.

Modules:
- extract_reads: Extracts reads based on i7 and i5 index pairs.
- concatenate_fastq: Concatenates and validates FASTQ files.

Usage:
    from local_demultiplexer import extract_reads, concatenate_fastq
"""

__version__ = "1.0.0"
__all__ = ["extract_reads", "concatenate_fastq"]
