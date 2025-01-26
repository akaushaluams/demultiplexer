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
    author='Akhilesh Kaushal',
    author_email='akhileshkaushal@gmail.com',
    description='A package for demultiplexing and processing FASTQ files.',
    license='MIT',
)