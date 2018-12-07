"""Unit test for disk space monitor"""

import unittest
import sys
from collections import namedtuple
from unittest.mock import Mock
import diskspacemonitor

class TestDiskSpaceMonitor(unittest.TestCase):
    """Testing Disk Space Monitor"""
    def test_parse_args(self):
        """Testing arg verification"""
        test_args = ["too", "many", "args"]
        self.assertEqual(diskspacemonitor.parse_args(test_args), 0)

        test_args = ["correct"]
        self.assertEqual(diskspacemonitor.parse_args(test_args), 1)

        test_args = ["also", "correct"]
        self.assertEqual(diskspacemonitor.parse_args(test_args), 1)

    def test_get_notification_percentages_nofile(self):
        """Test get a list of the notifications"""
        percentages = diskspacemonitor.get_notification_percentages("")
        self.assertGreater(len(percentages), 0)
        for index in range(len(percentages) - 1):
            self.assertLess(percentages[index], percentages[index+1])

    def test_get_notification_percentages(self):
        """Test get a list of the notifications"""
        percentages = diskspacemonitor.get_notification_percentages("prefs.txt")
        self.assertGreater(len(percentages), 0)
        for index in range(len(percentages) - 1):
            self.assertLess(percentages[index], percentages[index+1])

    def test_get_last_notification_value_no_file(self):
        """Test what the last notification was without a file"""
        self.assertEqual(diskspacemonitor.get_last_notification_value("nofile"), 100)

    def test_get_last_notification_value_with_file(self):
        """Test what the last notification was with a file"""
        self.assertEqual(diskspacemonitor.get_last_notification_value("testfile.txt"), 50)

# Do a test for file

    def test_parse_threshold(self):
        """Test if a value falls less than a range"""
        testlist = [10, 20, 90]
        self.assertEqual(diskspacemonitor.parse_threshold_list(testlist, 5), 10)
        self.assertEqual(diskspacemonitor.parse_threshold_list(testlist, 15), 20)
        self.assertEqual(diskspacemonitor.parse_threshold_list(testlist, 21), 90)
        self.assertEqual(diskspacemonitor.parse_threshold_list(testlist, 100), 100)

    def test_set_last_notification(self):
        """Test if a value falls less than a range"""
        diskspacemonitor.set_last_notification("writetest.txt", 50)
        testval = diskspacemonitor.get_last_notification_value("writetest.txt")
        self.assertEqual(50, testval)

    def test_process_disk_space(self):
        """Test the main crux of the code"""
        percentages = [90, 75, 10, 25, 5, 50, 15]
        percentages = sorted(percentages)
        TestType = namedtuple('Point', ['used', 'total', 'free'])
        testval = TestType(0, 200, 200)
        self.assertEqual(diskspacemonitor.process_disk_space(testval, 0, percentages), -1)
        testval = TestType(150, 200, 50)
        self.assertEqual(diskspacemonitor.process_disk_space(testval, 0, percentages), -1)
        # Testing that the last val was 50, new val is at 50% threshold, so return 0
        self.assertEqual(diskspacemonitor.process_disk_space(testval, 50, percentages), 25)
        testval = TestType(100, 200, 100)
        # Testing that the last val was 75, new val is at 50% threshold, so return 1
        self.assertEqual(diskspacemonitor.process_disk_space(testval, 75, percentages), 50)

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestDiskSpaceMonitor)
    RESULT = unittest.TextTestRunner(verbosity=2).run(SUITE)
    sys.exit(not RESULT.wasSuccessful())
