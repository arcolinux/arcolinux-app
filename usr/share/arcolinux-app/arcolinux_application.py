#!/usr/bin/env python3
# =================================================================
# =                  Author: Erik Dubois                          =
# =================================================================

from datetime import datetime
from time import sleep

import functions as fn
import gi
import gui
import splash

gi.require_version("Gtk", "3.0")

from gi.repository import GdkPixbuf, Gtk, GLib  # noqa

now = datetime.now()
global launchtime
# launchtime = file in /var/log
launchtime = now.strftime("%Y-%m-%d-%H-%M-%S")

if not fn.path.exists(fn.log_dir):
    fn.mkdir(fn.log_dir)

fn.create_actions_log(
    launchtime,
    "[INFO] %s App Started" % str(now) + "\n",
)

print("---------------------------------------------------------------------------")
print("[INFO] : pkgver = pkgversion")
print("[INFO] : pkgrel = pkgrelease")
print("---------------------------------------------------------------------------")
print("[INFO] : Distro = " + fn.distr)
print("---------------------------------------------------------------------------")

fn.create_actions_log(
    launchtime,
    "[INFO] %s pkgver = pkgversion" % str(now) + "\n",
)
fn.create_actions_log(
    launchtime,
    "[INFO] %s pkgrel = pkgrelease" % str(now) + "\n",
)

# making sure the tool follows a dark or light theme
if not fn.path.isdir("/root/.config/"):
    try:
        fn.mkdir("/root/.config", 0o766)
    except Exception as error:
        print(error)

if not fn.path.isdir("/root/.config/gtk-3.0"):
    try:
        fn.mkdir("/root/.config/gtk-3.0", 0o766)
    except Exception as error:
        print(error)

if not fn.path.isdir("/root/.config/gtk-4.0"):
    try:
        fn.mkdir("/root/.config/gtk-4.0", 0o766)
    except Exception as error:
        print(error)

if not fn.path.isdir("/root/.config/xsettingsd"):
    try:
        fn.mkdir("/root/.config/xsettingsd", 0o766)
    except Exception as error:
        print(error)

# make backup of /etc/pacman.conf
if fn.path.isfile(fn.pacman_conf):
    if not fn.path.isfile(fn.pacman_conf + ".bak"):
        try:
            fn.shutil.copy(fn.pacman_conf, fn.pacman_conf + ".bak")
            print("[INFO] : Making a backup of /etc/pacman.conf")
            fn.create_actions_log(
                launchtime,
                "[INFO] %s Making a backup of /etc/pacman.conf" % str(now) + "\n",
            )
        except Exception as error:
            print(error)

# ensuring we have a backup or the arcolinux mirrorlist
if fn.path.isfile(fn.mirrorlist):
    if not fn.path.isfile(fn.mirrorlist + ".bak"):
        try:
            fn.shutil.copy(fn.mirrorlist, fn.mirrorlist + ".bak")
            print("[INFO] : Making a backup of /etc/pacman.d/mirrorlist")
            fn.create_actions_log(
                launchtime,
                "[INFO] %s Making a backup of /etc/pacman.d/mirrorlist" % str(now)
                + "\n",
            )
        except Exception as error:
            print(error)


class Main(Gtk.Window):
    def __init__(self):
        super(Main, self).__init__(title="ArcoLinux App")
        self.set_border_width(10)
        self.set_default_size(900, 650)
        self.set_icon_from_file(fn.os.path.join(fn.base_dir, "images/arcolinux.png"))
        self.set_position(Gtk.WindowPosition.CENTER)
        self.timeout_id = None

        # splash screen
        splScr = splash.splashScreen()
        while Gtk.events_pending():
            Gtk.main_iteration()
        sleep(1)
        splScr.destroy()

        gui.GUI(self, Gtk, GdkPixbuf, fn)

    def on_close_clicked(self, widget):
        Gtk.main_quit()

    def on_create_arco_clicked(self, widget):
        now = datetime.now().strftime("%H:%M:%S")
        choice = self.iso_choices.get_active_text()
        print("[INFO] : Let's build an ArcoLinux iso : " + choice)
        fn.create_actions_log(
            launchtime,
            "[INFO] %s Let's build an ArcoLinux iso" % now + "\n",
        )
        # installing archiso if needed
        package = "archiso"
        fn.install_package(self, package)

        # if arcolinux mirror and key not installed
        if not fn.check_package_installed(
            "arcolinux-keyring"
        ) or not fn.check_package_installed("arcolinux-mirrorlist-git"):
            print("[INFO] : Installing the ArcoLinux keyring and mirrorlist")
            fn.create_actions_log(
                launchtime,
                "[INFO] %s Installing the ArcoLinux keyring and mirrorlist" % str(now)
                + "\n",
            )
            fn.install_arcolinux_key_mirror(self)
            fn.add_repos()
            self.arco_key_mirror.set_label("Remove")
            self.arco_key_mirror._value = 2

        # making sure we start with a clean slate
        print("[INFO] : Let's remove any old previous building folders")
        fn.remove_dir(self, "/root/ArcoLinux-Out")
        fn.remove_dir(self, "/root/ArcoLinuxB-Out")
        fn.remove_dir(self, "/root/ArcoLinuxD-Out")
        fn.remove_dir(self, "/root/arcolinux-build")
        fn.remove_dir(self, "/root/arcolinuxd-build")
        fn.remove_dir(self, "/root/arcolinuxb-build")

        # git clone the iso scripts

        if "b" in choice:
            print("[INFO] : Changing the B name")
            choice = choice.replace("linuxb", "")
            print("[INFO] : Renaming done to :" + choice)
            # B isos

            command = (
                "git clone https://github.com/arcolinuxb/" + choice + " /tmp/" + choice
            )
        else:
            # core isos
            command = (
                "git clone https://github.com/arcolinux/"
                + choice
                + "-iso /tmp/"
                + choice
            )
        print("[INFO] : git cloning the build folder")
        try:
            fn.run_command(command)
        except Exception as error:
            print(error)

        # launch the scripts
        # /tmp/arcolinuxd/installation-scripts/40-build-the-iso-local-again.sh

        print("[INFO] : Start building the iso in Alacritty")
        print(
            "[INFO] : #################################################################"
        )
        print("[INFO] : Sometimes you have to try and build it a second time")
        print(
            "[INFO] : for it to work because of the special packages from AUR and repos"
        )
        print(
            "[INFO] : ##################################################################"
        )

        print(
            "[INFO] : Changed to /tmp/" + choice + "/installation-scripts/" + " folder"
        )
        fn.os.chdir("/tmp/" + choice + "/installation-scripts/")

        command = (
            "/tmp/" + choice + "/installation-scripts/40-build-the-iso-local-again.sh"
        )

        print("[INFO] : Launching the building script")
        fn.create_actions_log(
            launchtime,
            "[INFO] %s Launching the building script" % str(now) + "\n",
        )

        if self.enable_hold.get_active():
            critty = "alacritty --hold -e"
            print("[INFO] : Using the hold option")
            fn.create_actions_log(
                launchtime,
                "[INFO] %s Using the hold option" % str(now) + "\n",
            )
        else:
            print("[INFO] : Not using the hold option")
            fn.create_actions_log(
                launchtime,
                "[INFO] %s Not using the hold option" % str(now) + "\n",
            )
            critty = "alacritty -e"

        try:
            fn.subprocess.call(
                critty + command,
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

        # if self.enable_hold.get_active():
        #     try:
        #         fn.subprocess.call(
        #             "alacritty --hold -e" + command,
        #             shell=True,
        #             stdout=fn.subprocess.PIPE,
        #             stderr=fn.subprocess.STDOUT,
        #         )
        #     except Exception as error:
        #         print(error)
        # else:
        #     try:
        #         fn.subprocess.call(
        #             "alacritty -e" + command,
        #             shell=True,
        #             stdout=fn.subprocess.PIPE,
        #             stderr=fn.subprocess.STDOUT,
        #         )
        #     except Exception as error:
        #         print(error)

        # move iso from /root/ArcoLinux-Out/ to home directory

        # change the foldername
        if (
            choice == "arcolinuxl"
            or choice == "arcolinuxs"
            or choice == "arcolinuxs-lts"
            or choice == "arcolinuxs-zen"
            or choice == "arcolinuxs-xanmod"
        ):
            dir = "ArcoLinux-Out"
        elif choice == "arcolinuxd":
            dir = "ArcoLinuxD-Out"
        else:
            dir = "ArcoLinuxB-Out"
        path_dir = "/root/" + dir
        destination = fn.home + "/" + dir
        print("[INFO] : Move folder to home directory")
        try:
            fn.shutil.copytree(path_dir, destination, dirs_exist_ok=True)
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "The creation of the ArcoLinux iso is finished",
                False,
            )
        except Exception as error:
            print(error)

        # changing permission
        fn.permissions(destination)
        print("[INFO] : Check your home directory for the iso")

    def on_create_arch_clicked(self, widget):
        now = datetime.now().strftime("%H:%M:%S")
        print("[INFO] : Let's build an Arch Linux iso")
        fn.create_actions_log(
            launchtime,
            "[INFO] %s Let's build an Arch Linux iso" % str(now) + "\n",
        )
        # installing archiso if needed
        package = "archiso"
        fn.install_package(self, package)

        # making sure we start with a clean slate
        if fn.path_check(fn.base_dir + "/work"):
            fn.remove_dir(self, "fn.base_dir" + "/work")
            print("[INFO] : Cleanup - Removing : " + fn.base_dir + "/work")
        if fn.path_check("/root/work"):
            fn.remove_dir(self, "/root/work")
            print("[INFO] : Cleanup - Removing : /root/work")

        # starting the build script
        command = "mkarchiso -v -o " + fn.home + " /usr/share/archiso/configs/releng/"
        fn.run_command(command)

        # changing permission
        x = fn.datetime.datetime.now()
        year = str(x.year)
        month = str(x.strftime("%m"))
        day = str(x.strftime("%d"))
        iso_name = "/archlinux-" + year + "." + month + "." + day + "-x86_64.iso"
        destination = fn.home + iso_name
        fn.permissions(destination)
        print("[INFO] : Check your home directory for the iso")

        # making sure we start with a clean slate
        if fn.path_check(fn.base_dir + "/work"):
            fn.remove_dir(self, "fn.base_dir" + "/work")
            print("[INFO] : Cleanup - Removing : " + fn.base_dir + "/work")
        if fn.path_check("/root/work"):
            fn.remove_dir(self, "/root/work")
            print("[INFO] : Cleanup - Removing : /root/work")

        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "The creation of the Arch Linux iso is finished",
            False,
        )

    def on_clean_pacman_cache_clicked(self, widget):
        now = datetime.now().strftime("%H:%M:%S")
        print("[INFO] : Let's clean the pacman cache")
        fn.create_actions_log(
            launchtime,
            "[INFO] %s Let's clean the pacman cache" % str(now) + "\n",
        )
        command = "yes | pacman -Scc"
        package = "alacritty"
        fn.install_package(self, package)
        try:
            fn.subprocess.call(
                command,
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("[INFO] : Pacman cache cleaned")
            fn.create_actions_log(
                launchtime,
                "[INFO] %s Pacman cache cleaned" % str(now) + "\n",
            )
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Pacman cache cleaned",
                False,
            )
        except Exception as error:
            print(error)

    def on_fix_arch_clicked(self, widget):
        now = datetime.now().strftime("%H:%M:%S")
        print("[INFO] : Let's fix the keys of Arch Linux")
        fn.create_actions_log(
            launchtime,
            "[INFO] %s Let's fix the keys of Arch Linux" % str(now) + "\n",
        )
        command = fn.base_dir + "/scripts/fixkey"
        package = "alacritty"
        fn.install_package(self, package)
        fn.run_script_alacritty_hold(self, command)
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Let's fix the keys of Arch Linux",
            False,
        )

    def on_probe_clicked(self, widget):
        now = datetime.now().strftime("%H:%M:%S")
        print("[INFO] : Let's create the probe link")
        fn.create_actions_log(
            launchtime,
            "[INFO] %s Let's create the probe link" % str(now) + "\n",
        )
        command = fn.base_dir + "/scripts/probe"
        package = "hw-probe"
        fn.install_package(self, package)
        fn.run_script_alacritty_hold(self, command)
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Creation of probe link is finished",
            False,
        )

    def on_get_nemesis_clicked(self, widget):
        now = datetime.now().strftime("%H:%M:%S")
        print("[INFO] : Get the ArcoLinux nemesis scripts")
        print("[INFO] : We create a DATA folder in your home dir")
        print("[INFO] : We git clone the scripts in there")
        fn.create_actions_log(
            launchtime,
            "[INFO] %s Get the ArcoLinux nemesis scripts" % str(now) + "\n",
        )
        command = fn.base_dir + "/scripts/get-nemesis-on-arcolinux-app"
        package = "alacritty"
        fn.install_package(self, package)
        fn.run_script(self, command)
        path_dir = "/root/DATA"
        destination = fn.home + "/DATA"
        # Move folder to home directory
        try:
            fn.shutil.copytree(path_dir, destination, dirs_exist_ok=True)
        except Exception as error:
            print(error)

        print("[INFO] : We saved the scripts to ~/DATA/arcolinux-nemesis")
        fn.create_actions_log(
            launchtime,
            "[INFO] %s We saved the scripts to ~/DATA/arcolinux-nemesis" % str(now)
            + "\n",
        )
        fn.permissions(destination)
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "We installed the ArcoLinux Nemesis scripts in ~/DATA",
            False,
        )

    def on_arch_server_clicked(self, widget):
        now = datetime.now().strftime("%H:%M:%S")
        print("[INFO] : Let's change the Arch Linux mirrors")
        fn.create_actions_log(
            launchtime,
            "[INFO] %s Let's change the Arch Linux mirrors" % str(now) + "\n",
        )
        command = fn.base_dir + "/scripts/best-arch-servers"
        package = "alacritty"
        fn.install_package(self, package)
        fn.run_script(self, command)
        print("[INFO] : We changed the content of your /etc/pacman.d/mirrorlist")
        print(
            "[INFO] : Server = http://mirror.rackspace.com/archlinux/\$repo/os/\$arch"
        )
        print(
            "[INFO] : Server = https://mirror.rackspace.com/archlinux/\$repo/os/\$arch"
        )
        print("[INFO] : Server = https://mirrors.kernel.org/archlinux/\$repo/os/\$arch")
        print("[INFO] : Server = https://mirror.osbeck.com/archlinux/\$repo/os/\$arch")
        print("[INFO] : Server = http://mirror.osbeck.com/archlinux/\$repo/os/\$arch")
        print("[INFO] : Server = https://geo.mirror.pkgbuild.com/\$repo/os/\$arch")
        print("[INFO] : Done")
        fn.create_actions_log(
            launchtime,
            "[INFO] %s We changed the content of your /etc/pacman.d/mirrorlist"
            % str(now)
            + "\n",
        )
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "We changed the content of your /etc/pacman.d/mirrorlist",
            False,
        )

    def on_arco_key_mirror_clicked_install(self, widget):
        now = datetime.now().strftime("%H:%M:%S")
        print("[INFO] : Let's install the ArcoLinux keys and mirrors")
        fn.create_actions_log(
            launchtime,
            "[INFO] %s Let's install the ArcoLinux keys and mirrors" % str(now) + "\n",
        )
        print("[INFO] : Installing the ArcoLinux repos in /etc/pacman.conf")
        fn.create_actions_log(
            launchtime,
            "[INFO] %s  Installing the ArcoLinux repos in /etc/pacman.conf" % str(now)
            + "\n",
        )
        fn.install_arcolinux_key_mirror(self)
        fn.add_repos()
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Installing the ArcoLinux repos in /etc/pacman.conf",
            False,
        )

    def on_arco_key_mirror_clicked_remove(self, widget):
        now = datetime.now().strftime("%H:%M:%S")
        print("[INFO] : Let's remove the ArcoLinux keys and mirrors")
        fn.create_actions_log(
            launchtime,
            "[INFO] %s Let's remove the ArcoLinux keys and mirrors" % str(now) + "\n",
        )
        fn.remove_arcolinux_key_mirror(self)
        print("[INFO] : Removing the ArcoLinux repos in /etc/pacman.conf")
        fn.create_actions_log(
            launchtime,
            "[INFO] %s  Removing the ArcoLinux repos in /etc/pacman.conf" % str(now)
            + "\n",
        )
        fn.remove_repos()
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Removing the ArcoLinux repos in /etc/pacman.conf",
            False,
        )

    def on_pacman_reset_local_clicked(self, widget):
        now = datetime.now().strftime("%H:%M:%S")
        if fn.path.isfile(fn.pacman_conf + ".bak"):
            fn.shutil.copy(fn.pacman_conf + ".bak", fn.pacman_conf)
            print(
                "[INFO] : We have used /etc/pacman.conf.bak to reset /etc/pacman.conf"
            )
            fn.create_actions_log(
                launchtime,
                "[INFO] %s We have used /etc/pacman.conf.bak to reset /etc/pacman.conf"
                % str(now)
                + "\n",
            )
            fn.pacman_safeguard()
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "We have used /etc/pacman.conf.bak to reset /etc/pacman.conf",
            False,
        )

    def on_pacman_reset_cached_clicked(self, widget):
        now = datetime.now().strftime("%H:%M:%S")
        fn.shutil.copy(fn.pacman_arco, fn.pacman_conf)
        if fn.distr == "arch":
            fn.shutil.copy(fn.pacman_arch, fn.pacman_conf)
        if fn.distr == "endeavouros":
            fn.shutil.copy(fn.pacman_eos, fn.pacman_conf)
        if fn.distr == "garuda":
            fn.shutil.copy(fn.pacman_garuda, fn.pacman_conf)
        print("[INFO] : We have used the cached pacman.conf")
        fn.create_actions_log(
            launchtime,
            "[INFO] %s We have used the cached pacman.conf" % str(now) + "\n",
        )
        fn.pacman_safeguard()
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "We have used the cached pacman.conf",
            False,
        )

    def on_find_path(self, widget):
        print("path")
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file",
            action=Gtk.FileChooserAction.OPEN,
        )
        filter = Gtk.FileFilter()
        filter.set_name("Text files")
        # filter.add_mime_type("image/png")
        # filter.add_mime_type("image/jpg")
        # filter.add_mime_type("image/jpeg")
        # dialog.set_filter(filter)
        dialog.set_current_folder(fn.home)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK
        )
        dialog.connect("response", self.open_response_cb)

        dialog.show()

    def open_response_cb(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            self.packages_path.set_text(dialog.get_filename())
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def on_pacman_install_packages(self, widget):
        now = datetime.now().strftime("%H:%M:%S")
        path = self.packages_path.get_text()
        if len(path) > 1 and not path == "Choose a file first":
            print("[INFO] : Installing packages from selected file")
            print("[INFO] : You selected this file")
            print("[INFO] : File: " + path)
            fn.create_actions_log(
                launchtime,
                "[INFO] %s Installing packages from selected file" % str(now) + "\n",
            )
            fn.create_actions_log(
                launchtime,
                "[INFO] %s You selected this file" % str(now) + "\n",
            )
            fn.create_actions_log(
                launchtime,
                "[INFO] %s File: " % str(now) + path + "\n",
            )
            fn.install_packages_path(self, self.packages_path.get_text())
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Packages installed from selected file",
                False,
            )
        else:
            print("[INFO] : First select a file")
            self.packages_path.set_text("Choose a file first")


if __name__ == "__main__":
    w = Main()
    w.connect("delete-event", Gtk.main_quit)
    w.show_all()
    Gtk.main()
