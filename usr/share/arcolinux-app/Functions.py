# =================================================================
# =           Author: Brad Heffernan                       =
# =================================================================

import os
import threading  # noqa
import subprocess
from pathlib import Path

base_dir = os.path.dirname(os.path.realpath(__file__))
working_dir = ''.join([str(Path(__file__).parents[2]),
                       "/share/hefftor-welcome-app/"])
proc = subprocess.Popen(["who"], stdout=subprocess.PIPE, shell=True, executable='/bin/bash') # noqa
users = proc.stdout.readlines()[0].decode().strip().split(" ")[0]
print(users)
DEBUG = False

if DEBUG:
    config = "/home/bheffernan/Repos/GITS/HLWM/hefftor-calamares-config-herbstluftwm/calamares-basic/modules/partition.conf"  # noqa
    liveuser = users
else:
    config = "/etc/calamares/modules/partition.conf"
    liveuser = "liveuser"

fs = [
    'btrfs',
    'xfs',
    'jfs',
    'reiser',
    'f2fs',
    'ext4',
]

message = "The ArcoLinux Calamares tool is only for the live ISO"  # noqa


def __get_position(lists, string):
    data = [x for x in lists if string in x]
    pos = lists.index(data[0])
    return pos


def set_config(string):
    with open(config, "r") as f:
        lines = f.readlines()
        f.close()

    pos = __get_position(lines, "defaultFileSystemType:")

    lines[pos] = "defaultFileSystemType:  \"" + string + "\"\n"

    with open(config, "w") as f:
        f.writelines(lines)
        f.close()
