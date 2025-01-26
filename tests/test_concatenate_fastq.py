import unittest
from local_demultiplexer.concatenate_fastq import FastqConcatenator

class TestFastqConcatenator(unittest.TestCase):
    def test_concatenation(self):
        concatenator = FastqConcatenator("test_R1", "test_R2", "output", "test.log")
        self.assertTrue(hasattr(concatenator, 'concatenate_files'))

if __name__ == '__main__':
    unittest.main()
