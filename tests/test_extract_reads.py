import unittest
from local_demultiplexer.extract_reads import FastqExtractor

class TestFastqExtractor(unittest.TestCase):
    def test_extraction(self):
        extractor = FastqExtractor("test.fastq.gz", "index_pairs.txt", "output")
        self.assertTrue(hasattr(extractor, 'extract_reads'))

if __name__ == '__main__':
    unittest.main()