"""Unit test for disk space monitor"""

import unittest
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

    @unittest.mock.patch('shutil.disk_usage')
    def test_get_disk_space(self, mock_shutil):
        """Test get disk space"""
        testval = {"used": 100, "total": 200, "free": 300}
        mock_shutil.return_value = testval
        self.assertEqual(diskspacemonitor.get_disk_space("anything"), testval)

    @unittest.mock.patch('shutil.disk_usage', side_effect=IOError())
    def test_get_disk_space_fail(self, mock_shutil):
        """Test fail to get disk space"""
        self.assertEqual(diskspacemonitor.get_disk_space("anything"), 0)

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

    def test_get_disk_space_percentage(self):
        """Test get the disk space percentage"""
        TestType = namedtuple('Point', ['used', 'total', 'free'])
        testval = TestType(100, 200, 100)
        self.assertEqual(diskspacemonitor.get_disk_space_percentage(testval), 50)
        testval = TestType(100, 400, 300)
        self.assertEqual(diskspacemonitor.get_disk_space_percentage(testval), 75)

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
        self.assertEqual(diskspacemonitor.process_disk_space(testval, 0, percentages), -100)
        testval = TestType(150, 200, 50)
        self.assertEqual(diskspacemonitor.process_disk_space(testval, 0, percentages), -25)
        # Testing that the last val was 50, new val is at 50% threshold, so return 0
        self.assertEqual(diskspacemonitor.process_disk_space(testval, 50, percentages), 25)
        testval = TestType(100, 200, 100)
        # Testing that the last val was 75, new val is at 50% threshold, so return 1
        self.assertEqual(diskspacemonitor.process_disk_space(testval, 75, percentages), 50)
        # Testing that the last val was less than the new one - disk has been emptied
        testval = TestType(100, 200, 100)
        self.assertEqual(diskspacemonitor.process_disk_space(testval, 10, percentages), -50)

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestDiskSpaceMonitor)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
