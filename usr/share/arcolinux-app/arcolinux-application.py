#!/usr/bin/env python3
# =================================================================
# =                  Author: Erik Dubois                          =
# =================================================================

import gi
import gui
import splash
import functions as fn
from time import sleep

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GdkPixbuf  # noqa

print("---------------------------------------------------------------------------")
print("[INFO] : pkgver = pkgversion")
print("[INFO] : pkgrel = pkgrelease")
print("---------------------------------------------------------------------------")
print("[INFO] : Distro = " + fn.distr)
print("---------------------------------------------------------------------------")


class Main(Gtk.Window):
    def __init__(self):
        super(Main, self).__init__(title="ArcoLinux App")
        self.set_border_width(10)
        self.set_default_size(750, 400)
        self.set_icon_from_file(fn.os.path.join(fn.base_dir, "images/arcolinux.png"))
        self.set_position(Gtk.WindowPosition.CENTER)

        # splash screen
        splScr = splash.splashScreen()
        while Gtk.events_pending():
            Gtk.main_iteration()
        sleep(1)
        splScr.destroy()

        gui.GUI(self, Gtk, GdkPixbuf, fn)

    def on_close_clicked(self, widget):
        Gtk.main_quit()

    def on_save_clicked(self, widget):
        t = fn.threading.Thread(
            target=fn.set_config, args=(self.fileSystem.get_active_text(),)
        )
        t.daemon = True
        t.start()

    def on_create_arco_clicked(self, widget):
        choice = self.iso_choices.get_active_text()
        print("[INFO] : Let's build an ArcoLinux iso : " + choice)
        # installing archiso if needed
        package = "archiso"
        fn.install_package(self, package)

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
        try:
            fn.subprocess.call(
                "alacritty -e" + command,
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

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
        except Exception as error:
            print(error)

        # changing permission
        fn.permissions(destination)
        print("[INFO] : Check your home directory for the iso")

    def on_create_arch_clicked(self, widget):
        print("[INFO] : Let's build an Arch Linux iso")
        # installing archiso if needed
        package = "archiso"
        fn.install_package(self, package)

        # making sure we start with a clean slate
        fn.remove_dir(self, fn.base_dir + "/work")
        fn.remove_dir(self, "/root/work")

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
        fn.remove_dir(self, fn.base_dir + "/work")
        fn.remove_dir(self, "/root/work")

    def on_fix_arch_clicked(self, widget):
        print("[INFO] : Let's fix the keys of Arch Linux")
        command = fn.base_dir + "/scripts/fixkey"
        package = "alacritty"
        fn.install_package(self, package)
        fn.run_script_alacritty(self, command)

    def on_arch_server_clicked(self, widget):
        print("[INFO] : Let's change the Arch Linux mirrors")
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

    def on_arco_key_mirror_clicked(self, widget):
        if self.arco_key_mirror._value == 1:
            print("[INFO] : Let's install the ArcoLinux keys and mirrors")
            fn.install_arcolinux_key_mirror(self)
            fn.add_repos()
            self.arco_key_mirror.set_label("Remove")
            self.arco_key_mirror._value = 2
        else:
            print("[INFO] : Let's remove the ArcoLinux keys and mirrors")
            fn.remove_arcolinux_key_mirror(self)
            print("[INFO] : Removing the ArcoLinux repos in /etc/pacman.conf")
            fn.remove_repos()
            self.arco_key_mirror.set_label("Install")
            self.arco_key_mirror._value = 1


if __name__ == "__main__":
    w = Main()
    w.connect("delete-event", Gtk.main_quit)
    w.show_all()
    Gtk.main()
