#non_zk_index_tests
import unittest
from protocols.non_zk_index import create_stream, non_zk_index_protocol

class TestClass(unittest.TestCase):
    def create_stream(self):
        input1 = create_stream("input1.txt", [1,2,3,4,2,5,6,7,9,11], 2)
        print(input1)
    def non_zk_test_one(self):
        input = [10,1,2,3,4,2,5,6,7,9,11,2]
        self.assertEqual(non_zk_index_protocol(input), 2)

