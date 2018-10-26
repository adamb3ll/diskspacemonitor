"""Simply gets the disk free space as % and returns it"""

import shutil
import sys

def parse_args(argv):
    """Confirm params are correct"""
    return len(argv) == 1

def get_disk_space(disk):
    """Get the disk space and return if Successful"""
    try:
        usage = shutil.disk_usage(disk)
        return usage
    except IOError:
        return 0

def get_disk_space_percentage(disk_space):
    """Get the disk space remaining as a percentage"""
    perc = (disk_space.free * 100) / disk_space.total
    return perc

def main(argv):
    """"Main function"""
    disk = "/"
    if parse_args(argv) == 1:
        disk = argv[0]

    space = get_disk_space(disk)
    percfree = get_disk_space_percentage(space)
    sys.exit(int(percfree))

if __name__ == "__main__":
    main(sys.argv[1:])
