# =================================================================
# =                  Author: Erik Dubois                          =
# =================================================================

import datetime
import os
import shutil
import subprocess
from os import getlogin, listdir, mkdir, path, rmdir
from pathlib import Path

import psutil
from distro import id
from gi.repository import GLib

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
mirrorlist = "/etc/pacman.d/mirrorlist"
log_dir = "/var/log/arcolinux-app/"
pacman_conf = "/etc/pacman.conf"
pacman_arch = "/usr/share/arcolinux-app/data/arch/pacman.conf"
pacman_arco = "/usr/share/arcolinux-app/data/arco/pacman.conf"
pacman_eos = "/usr/share/arcolinux-app/data/eos/pacman.conf"
pacman_garuda = "/usr/share/arcolinux-app/data/garuda/pacman.conf"

atestrepo = "#[arcolinux_repo_testing]\n\
#SigLevel = Optional TrustedOnly\n\
#Include = /etc/pacman.d/arcolinux-mirrorlist"

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


# check if repo exists
def repo_exist(value):
    """check repo_exists"""
    with open(pacman_conf, "r", encoding="utf-8") as f:
        lines = f.readlines()
        f.close()

    for line in lines:
        if value in line:
            return True
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
        command1 = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        print("[INFO] : " + command1)
        subprocess.call(
            command1.split(" "),
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
        command2 = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        print("[INFO] : " + command2)
        subprocess.call(
            command2.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("[INFO] : ArcoLinux mirrorlist is now installed")
    except Exception as error:
        print(error)


# remove ArcoLinux mirrorlist and key package
def remove_arcolinux_key_mirror(self):
    try:
        command1 = "pacman -Rdd arcolinux-keyring --noconfirm"
        print("[INFO] : " + command1)
        subprocess.call(
            command1.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("[INFO] : ArcoLinux keyring is now removed")
    except Exception as error:
        print(error)

    try:
        command2 = "pacman -Rdd arcolinux-mirrorlist-git --noconfirm"
        print("[INFO] : " + command2)
        subprocess.call(
            command2.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("[INFO] : ArcoLinux mirrorlist is now removed")
    except Exception as error:
        print(error)


def pacman_safeguard():
    package = "arcolinux-mirrorlist-git"
    if not check_package_installed(package):
        print("[INFO] : Removing the lines referring to the ArcoLinux repos")
        remove_repos()


def run_script(self, command):
    print("[INFO] : Applying this command")
    print("[INFO] : " + command)
    try:
        subprocess.call(
            command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
    except Exception as error:
        print(error)


def run_script_alacritty_hold(self, command):
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


def run_script_alacritty(self, command):
    print("[INFO] : Applying this command")
    print("[INFO] : " + command)
    try:
        subprocess.call(
            "alacritty -e" + command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except Exception as error:
        print(error)


def run_command(command):
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


def append_repo(text):
    """Append a new repo"""
    try:
        with open(pacman_conf, "a", encoding="utf-8") as f:
            f.write("\n\n")
            f.write(text)
    except Exception as error:
        print(error)


def add_repos():
    if not repo_exist("[arcolinux_repo]"):
        if distr == "arcolinux":
            print("[INFO] : Adding ArcoLinux repos on ArcoLinux")
            try:
                with open(pacman_conf, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    f.close()
            except Exception as error:
                print(error)

            text = (
                "\n\n"
                + atestrepo
                + "\n\n"
                + arepo
                + "\n\n"
                + a3prepo
                + "\n\n"
                + axlrepo
                + "\n\n"
            )

            pos = get_position(lines, "#[testing]")
            lines.insert(pos - 2, text)

            try:
                with open(pacman_conf, "w", encoding="utf-8") as f:
                    f.writelines(lines)
            except Exception as error:
                print(error)
        else:
            if not repo_exist("[arcolinux_repo_testing]"):
                print("[INFO] : Adding ArcoLinux test repo (not used)")
                append_repo(atestrepo)
            if not repo_exist("[arcolinux_repo]"):
                print("[INFO] : Adding ArcoLinux repo")
                append_repo(arepo)
            if not repo_exist("[arcolinux_repo_3party]"):
                print("[INFO] : Adding ArcoLinux 3th party repo")
                append_repo(a3prepo)
            if not repo_exist("[arcolinux_repo_xlarge]"):
                print("[INFO] : Adding ArcoLinux XL repo")
                append_repo(axlrepo)
            if repo_exist("[arcolinux_repo]"):
                print("[INFO] : ArcoLinux repos have been installed")


def remove_repos():
    """remove the repo"""
    try:
        with open(pacman_conf, "r", encoding="utf-8") as f:
            lines = f.readlines()
            f.close()

        if repo_exist("[arcolinux_repo_testing]"):
            pos = get_position(lines, "[arcolinux_repo_testing]")
            del lines[pos + 3]
            del lines[pos + 2]
            del lines[pos + 1]
            del lines[pos]

        if repo_exist("[arcolinux_repo]"):
            pos = get_position(lines, "[arcolinux_repo]")
            del lines[pos + 3]
            del lines[pos + 2]
            del lines[pos + 1]
            del lines[pos]

        if repo_exist("[arcolinux_repo_3party]"):
            pos = get_position(lines, "[arcolinux_repo_3party]")
            del lines[pos + 3]
            del lines[pos + 2]
            del lines[pos + 1]
            del lines[pos]

        if repo_exist("[arcolinux_repo_xlarge]"):
            pos = get_position(lines, "[arcolinux_repo_xlarge]")
            del lines[pos + 2]
            del lines[pos + 1]
            del lines[pos]

        with open(pacman_conf, "w", encoding="utf-8") as f:
            f.writelines(lines)
            f.close()

    except Exception as error:
        print(error)


# =====================================================
#                     LOGGING
# =====================================================


def create_actions_log(launchtime, message):
    if not os.path.exists(log_dir + launchtime):
        try:
            with open(log_dir + launchtime, "x", encoding="utf8") as f:
                f.close
        except Exception as error:
            print(error)

    if os.path.exists(log_dir + launchtime):
        try:
            with open(log_dir + launchtime, "a", encoding="utf-8") as f:
                f.write(message)
                f.close()
        except Exception as error:
            print(error)


def install_packages_path(self, path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            f.close()
    except Exception as error:
        print(error)

    for line in lines:
        line = line.strip("\n")
        if not line.find("#") != -1:
            install_package(self, line)


# =====================================================
#               NOTIFICATIONS
# =====================================================


def show_in_app_notification(self, message, err):
    if self.timeout_id is not None:
        GLib.source_remove(self.timeout_id)
        self.timeout_id = None

    if err == True:
        self.notification_label.set_markup(
            '<span background="yellow" foreground="black">' + message + "</span>"
        )
    else:
        self.notification_label.set_markup(
            '<span foreground="white">' + message + "</span>"
        )
    self.notification_revealer.set_reveal_child(True)
    self.timeout_id = GLib.timeout_add(3000, timeOut, self)


def timeOut(self):
    close_in_app_notification(self)


def close_in_app_notification(self):
    self.notification_revealer.set_reveal_child(False)
    GLib.source_remove(self.timeout_id)
    self.timeout_id = None
