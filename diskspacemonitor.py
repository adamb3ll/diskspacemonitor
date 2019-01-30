"""Sends notification if hard drive hits a free space milestone"""

import shutil
import sys
import os
from collections import namedtuple
import requests
import pushnotifications
import diskspace

def parse_args(argv):
    """Confirm params are correct"""
    return len(argv) == 1 or len(argv) == 2

def get_notification_percentages(filename):
    """Get a list of the percentages of when there should be a notification"""
    #percentages = [10, 25, 5, 50, 15]
    percentages = [90, 75, 10, 25, 5, 50, 15]

    try:
        currentdir = os.getcwd()
        with open(currentdir + "/" + filename, 'r') as file:
            percentages.clear()
            for line in file:
                percentages.append(int(line.rstrip('\n')))
    except IOError:
        print("Unknown notification file")

    percentages = sorted(percentages)
    return percentages

def get_last_notification_value(filename):
    """Get the last time a notification was sent"""
    try:
        currentdir = os.getcwd()
        with open(currentdir + "/" + filename, 'r') as file:
            val = int(file.readline())
            return val
    except IOError:
        return 100

def set_last_notification(filename, value):
    """Set the last time a notification was sent"""
    try:
        currentdir = os.getcwd()
        with open(currentdir + "/" + filename, 'w') as file:
            file.write(str(value))
            return 1
    except IOError:
        return 0

def parse_threshold_list(parselist, current):
    """Parse where the value lands on the require threshold"""
    for index in range(len(parselist)):
        if current <= parselist[index]:
            return parselist[index]
    return 100

def process_disk_space(space, lastval, notification_percs):
    """Process all the data, is space getting low and must notify"""
    if space != 0:
        perc = diskspace.get_disk_space_percentage(space)
        newval = parse_threshold_list(notification_percs, perc)
        if newval < lastval:
            return newval
        return -1
    return 100

def main(argv):
    """"Main function"""
    disk = "/"
    disk_id = "Computer"
    if parse_args(argv) == 1 and len(argv) == 2:
        disk = argv[0]
    if parse_args(argv) == 1 and len(argv) == 2:
        disk_id = argv[1]

    space = diskspace.get_disk_space(disk)
    if space != 0:
        filename = disk_id + "_last.dsm"
        lastval = get_last_notification_value(filename)
        notification_prefs = get_notification_percentages("prefs.txt")
        newval = process_disk_space(space, lastval, notification_prefs)
        if newval != -1:
            set_last_notification(filename, newval)
            if newval != 100:
                pushnotifications.push_notification(disk_id + " Disk Milestone Reached", "Disk free space is now below " + str(newval) + "%")
    else:
        print("Invalid Disk:", disk)

if __name__ == "__main__":
    main(sys.argv[1:])


# get disk space of disk
# get datafile of last notification value
# get disk space as percentages
# if percentage crosses new threshold that is less than recorded
# send notification
# update data file with new threshold percentage
