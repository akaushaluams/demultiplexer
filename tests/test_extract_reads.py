import unittest
import os
from local_demultiplexer.extract_reads import FastqExtractor

class TestFastqExtractor(unittest.TestCase):
    def test_extraction(self):
        test_dir = os.path.join(os.path.dirname(__file__), "test_data")
        extractor = FastqExtractor(
            os.path.join(test_dir, "test.fastq.gz"),
            os.path.join(test_dir, "index_pairs.txt"),
            "output"
        )
        self.assertTrue(hasattr(extractor, 'extract_reads'))

if __name__ == '__main__':
    unittest.main()
