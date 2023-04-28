# =================================================================
# =                  Author: Erik Dubois                          =
# =================================================================


def GUI(self, Gtk, GdkPixbuf, fn):
    # ======================================================================
    #                   CONTAINERS
    # ======================================================================

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

    hbox_logo = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    # hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    # ======================================================================
    #                           HBOX_LOGO
    # ======================================================================

    img_pb = GdkPixbuf.Pixbuf().new_from_file_at_size(
        fn.os.path.join(
            str(fn.Path(__file__).parent), "images/arcolinux-one-liner.png"
        ),
        235,
        235,
    )  # noqa
    img = Gtk.Image().new_from_pixbuf(img_pb)
    hbox_logo.pack_start(img, True, False, 0)

    # ======================================================================
    #                           HBOX 1
    # ======================================================================

    lbl_create_arch = Gtk.Label(label="Create your personal Arch Linux iso: ")
    self.create_arch = Gtk.Button(label="Create")
    self.create_arch.set_size_request(280, 0)

    hbox1.pack_start(lbl_create_arch, False, False, 0)
    hbox1.pack_end(self.create_arch, False, False, 0)

    # ======================================================================
    #                           HBOX 2
    # ======================================================================

    lbl_create_arch = Gtk.Label(label="Create your personal Arch Linux iso: ")
    self.create_arch = Gtk.Button(label="Create")
    self.create_arch.set_size_request(280, 0)

    hbox2.pack_start(lbl_create_arch, False, False, 0)
    hbox2.pack_end(self.create_arch, False, False, 0)

    # # ======================================================================
    # #                            HBOX2
    # # ======================================================================

    # lblmessage = Gtk.Label()
    # lblmessage.set_justify(Gtk.Justification.CENTER)
    # lblmessage.set_line_wrap(True)
    # lblmessage.set_markup(
    #     '<span foreground="orange" size="xx-large">' + fn.message + "</span>"
    # )  # noqa

    # hbox2.pack_start(lblmessage, True, False, 0)

    # ======================================================================
    #                       HBOX_BUTTONS
    # ======================================================================

    btnCancel = Gtk.Button(label="Close")
    btnCancel.connect("clicked", self.on_close_clicked)
    btnOK = Gtk.Button(label="Save")
    btnOK.connect("clicked", self.on_save_clicked)

    hbox_buttons.pack_end(btnCancel, False, False, 0)
    hbox_buttons.pack_end(btnOK, False, False, 0)

    # ======================================================================
    #                   PACK TO WINDOW
    # ======================================================================

    scrolledWindow = Gtk.ScrolledWindow()
    self.add(scrolledWindow)

    vbox.pack_start(hbox_logo, False, False, 20)  # LOGO
    vbox.pack_start(hbox1, False, False, 0)
    vbox.pack_start(hbox2, False, False, 20)
    vbox.pack_end(hbox_buttons, False, False, 7)  # Buttons

    scrolledWindow.add(vbox)
