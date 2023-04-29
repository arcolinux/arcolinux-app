# =================================================================
# =                  Author: Erik Dubois                          =
# =================================================================

import os
import subprocess
import psutil
import shutil
import datetime
from pathlib import Path
from distro import id
from os import getlogin, path, mkdir, rmdir, listdir

DEBUG = False

# =====================================================
#              BEGIN DECLARATION OF VARIABLES
# =====================================================

base_dir = path.dirname(path.realpath(__file__))
distr = id()
sudo_username = getlogin()
home = "/home/" + str(sudo_username)
message = "This is the ArcoLinux App"
arcolinux_mirrorlist = "/etc/pacman.d/arcolinux-mirrorlist"
pacman_conf = "/etc/pacman.conf"

atestrepo = "[arcolinux_repo_testing]\n\
SigLevel = Optional TrustedOnly\n\
Include = /etc/pacman.d/arcolinux-mirrorlist"

arepo = "[arcolinux_repo]\n\
SigLevel = Optional TrustedOnly\n\
Include = /etc/pacman.d/arcolinux-mirrorlist"

a3prepo = "[arcolinux_repo_3party]\n\
SigLevel = Optional TrustedOnly\n\
Include = /etc/pacman.d/arcolinux-mirrorlist"

axlrepo = "[arcolinux_repo_xlarge]\n\
SigLevel = Optional TrustedOnly\n\
Include = /etc/pacman.d/arcolinux-mirrorlist"

# =====================================================
#              END DECLARATION OF VARIABLES
# =====================================================


# =====================================================
#               BEGIN GLOBAL FUNCTIONS
# =====================================================


# getting the content of a file
def get_lines(files):
    try:
        if path.isfile(files):
            with open(files, "r", encoding="utf-8") as f:
                lines = f.readlines()
                f.close()
            return lines
    except Exception as error:
        print(error)


def __get_position(lists, string):
    data = [x for x in lists if string in x]
    pos = lists.index(data[0])
    return pos


# get position in list
def get_position(lists, value):
    data = [string for string in lists if value in string]
    if len(data) != 0:
        position = lists.index(data[0])
        return position
    return 0


# get positions in list
def get_positions(lists, value):
    data = [string for string in lists if value in string]
    position = []
    for d in data:
        position.append(lists.index(d))
    return position


# check if process is running
def check_if_process_is_running(processName):
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=["pid", "name", "create_time"])
            if processName == pinfo["name"]:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


# check value in list
def check_value(list, value):
    data = [string for string in list if value in string]
    return data


# check if value is true or false in file
def check_content(value, file):
    try:
        with open(file, "r", encoding="utf-8") as myfile:
            lines = myfile.readlines()
            myfile.close()

        for line in lines:
            if value in line:
                if value in line:
                    return True
                else:
                    return False
        return False
    except:
        return False


# check if package is installed or not
def check_package_installed(package):
    try:
        subprocess.check_output(
            "pacman -Qi " + package, shell=True, stderr=subprocess.STDOUT
        )
        # package is installed
        return True
    except subprocess.CalledProcessError:
        # package is not installed
        return False


# install package
def install_package(self, package):
    command = "pacman -S " + package + " --noconfirm --needed"
    # if more than one package - checf fails and will install
    if check_package_installed(package):
        print(
            "[INFO] : The package " + package + " is already installed - nothing to do"
        )
    else:
        try:
            print("[INFO] : Applying this command - " + command)
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            print("[INFO] : The package " + package + " is now installed")
        except Exception as error:
            print(error)


# install ArcoLinux mirrorlist and key package
def install_arcolinux_key_mirror(self):
    base_dir = path.dirname(path.realpath(__file__))
    pathway = base_dir + "/packages/arcolinux-keyring/"
    file = listdir(pathway)

    try:
        install = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        print("[INFO] : " + install)
        subprocess.call(
            install.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("[INFO] : ArcoLinux keyring is now installed")
    except Exception as error:
        print(error)

    pathway = base_dir + "/packages/arcolinux-mirrorlist/"
    file = listdir(pathway)
    try:
        install = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        print("[INFO] : " + install)
        subprocess.call(
            install.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("[INFO] : ArcoLinux mirrorlist is now installed")
    except Exception as error:
        print(error)


def run_script(self, command):
    print("[INFO] : Applying this command")
    print("[INFO] : " + command)
    try:
        subprocess.call(
            command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
    except Exception as error:
        print(error)


def run_script_alacritty(self, command):
    print("[INFO] : Applying this command")
    print("[INFO] : " + command)
    try:
        subprocess.call(
            "alacritty --hold -e" + command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except Exception as error:
        print(error)


def run_command(self, command):
    print("[INFO] : Applying this command")
    print("[INFO] : " + command)
    try:
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except Exception as error:
        print(error)


# check if path exists
def path_check(path):
    if os.path.isdir(path):
        return True
    return False


def remove_dir(self, directory):
    if path_check(directory):
        try:
            shutil.rmtree(directory)
        except Exception as error:
            print(error)


def permissions(dst):
    try:
        groups = subprocess.run(
            ["sh", "-c", "id " + sudo_username],
            check=True,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        for x in groups.stdout.decode().split(" "):
            if "gid" in x:
                g = x.split("(")[1]
                group = g.replace(")", "").strip()
        subprocess.call(["chown", "-R", sudo_username + ":" + group, dst], shell=False)
    except Exception as error:
        print(error)


# =====================================================
#               END GLOBAL FUNCTIONS
# =====================================================

# =====================================================
#               START PACMAN.CONF
# =====================================================


def append_repo(self, text):
    """Append a new repo"""
    try:
        with open(pacman_conf, "a", encoding="utf-8") as f:
            f.write("\n\n")
            f.write(text)
    except Exception as error:
        print(error)


def repo_exist(value):
    """check repo_exists"""
    with open(pacman_conf, "r", encoding="utf-8") as f:
        lines = f.readlines()
        f.close()

    for line in lines:
        if value in line:
            return True
    return False
