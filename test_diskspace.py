"""Unit test for disk space"""

import unittest
import sys
from unittest.mock import Mock
from collections import namedtuple
import diskspace

class TestDiskSpace(unittest.TestCase):
    """Testing Disk Space"""
    def test_parse_args(self):
        """Testing arg verification"""
        test_args = ["too", "many", "args"]
        self.assertEqual(diskspace.parse_args(test_args), 0)

        test_args = ["correct"]
        self.assertEqual(diskspace.parse_args(test_args), 1)

    @unittest.mock.patch('shutil.disk_usage')
    def test_get_disk_space(self, mock_shutil):
        """Test get disk space"""
        testval = {"used": 100, "total": 200, "free": 300}
        mock_shutil.return_value = testval
        self.assertEqual(diskspace.get_disk_space("anything"), testval)

    @unittest.mock.patch('shutil.disk_usage', side_effect=IOError())
    def test_get_disk_space_fail(self, mock_shutil):
        """Test fail to get disk space"""
        self.assertEqual(diskspace.get_disk_space("anything"), 0)

    def test_get_disk_space_percentage(self):
        """Test get the disk space percentage"""
        TestType = namedtuple('Point', ['used', 'total', 'free'])
        testval = TestType(100, 200, 100)
        self.assertEqual(diskspace.get_disk_space_percentage(testval), 50)
        testval = TestType(100, 400, 300)
        self.assertEqual(diskspace.get_disk_space_percentage(testval), 75)

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestDiskSpace)
    RESULT = unittest.TextTestRunner(verbosity=2).run(SUITE)
    sys.exit(not RESULT.wasSuccessful())
