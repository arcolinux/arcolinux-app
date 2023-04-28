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
        self.set_default_size(560, 250)
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

    def on_create_arch_clicked(self, widget):
        print("[INFO] : Let's build an Arch Linux iso")
        package = "archiso"
        fn.install_package(self, package)
        command = "sudo mkarchiso -v /usr/share/archiso/configs/releng/ -o " + fn.home
        fn.run_command(self, command)

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


if __name__ == "__main__":
    w = Main()
    w.connect("delete-event", Gtk.main_quit)
    w.show_all()
    Gtk.main()
