#!/usr/bin/env python3
# =================================================================
# =                  Author: Brad Heffernan                       =
# =================================================================
import gi
import GUI
import Functions as fn

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf  # noqa


class Main(Gtk.Window):
    def __init__(self):
        super(Main, self).__init__(title="ArcoLinux Calamares Tool")
        self.set_border_width(10)
        self.set_default_size(560, 250)
        self.set_icon_from_file(fn.os.path.join(
            fn.base_dir, 'images/arcolinux.png'))
        self.set_position(Gtk.WindowPosition.CENTER)

        GUI.GUI(self, Gtk, GdkPixbuf, fn)

    def on_close_clicked(self, widget):
        Gtk.main_quit()

    def on_save_clicked(self, widget):
        t = fn.threading.Thread(target=fn.set_config,
                                args=(self.fileSystem.get_active_text(),))
        t.daemon = True
        t.start()


if __name__ == "__main__":
    w = Main()
    w.connect("delete-event", Gtk.main_quit)
    w.show_all()
    Gtk.main()
