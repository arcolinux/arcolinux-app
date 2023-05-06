# =================================================================
# =                  Author: Erik Dubois                          =
# =================================================================


def GUI(self, Gtk, GdkPixbuf, fn):
    # ======================================================================
    #                   CONTAINERS
    # ======================================================================
    hbox_revealer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

    hbox_logo = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox0 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox6 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox7 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox8 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox9 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_message = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    # =======================================================
    #                       App Notifications
    # =======================================================

    hbox_revealer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    self.notification_revealer = Gtk.Revealer()
    self.notification_revealer.set_reveal_child(False)

    self.notification_label = Gtk.Label()

    pb_panel = GdkPixbuf.Pixbuf().new_from_file(fn.base_dir + "/images/panel.png")
    panel = Gtk.Image().new_from_pixbuf(pb_panel)

    overlayFrame = Gtk.Overlay()
    overlayFrame.add(panel)
    overlayFrame.add_overlay(self.notification_label)

    self.notification_revealer.add(overlayFrame)

    hbox_revealer.pack_start(self.notification_revealer, True, False, 0)

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
    #                           HBOX 0
    # ======================================================================

    lbl_create_arco = Gtk.Label(label="Create your personal ArcoLinux iso: ")
    self.iso_choices = Gtk.ComboBoxText()
    options = [
        "arcolinuxl",
        "arcolinuxd",
        "arcolinuxs",
        "arcolinuxs-lts",
        "arcolinuxs-zen",
        "arcolinuxs-xanmod",
        "arcolinuxb-awesome",
        "arcolinuxb-berry",
        "arcolinuxb-bspwm",
        "arcolinuxb-budgie",
        "arcolinuxb-chadwm",
        "arcolinuxb-cinnamon",
        "arcolinuxb-cutefish",
        "arcolinuxb-cwm",
        "arcolinuxb-deepin",
        "arcolinuxb-dusk",
        "arcolinuxb-dwm",
        "arcolinuxb-fvwm3",
        "arcolinuxb-gnome",
        "arcolinuxb-herbstluftw",
        "arcolinuxb-hyprland",
        "arcolinuxb-i3",
        "arcolinuxb-icewm",
        "arcolinuxb-jwm",
        "arcolinuxb-leftwm",
        "arcolinuxb-lxqt",
        "arcolinuxb-mate",
        "arcolinuxb-openbox",
        "arcolinuxb-pantheon",
        "arcolinuxb-plasma",
        "arcolinuxb-qtile",
        "arcolinuxb-spectrwm",
        "arcolinuxb-sway",
        "arcolinuxb-ukui",
        "arcolinuxb-wmderland",
        "arcolinuxb-worm",
        "arcolinuxb-xfce",
        "arcolinuxb-xmonad",
        "arcolinuxb-xtended",
    ]
    for option in options:
        self.iso_choices.append_text(option)
    self.iso_choices.set_active(0)
    self.iso_choices.set_wrap_width(1)

    self.enable_hold = Gtk.CheckButton(label="hold")

    self.create_arco = Gtk.Button(label="Create")
    self.create_arco.set_size_request(280, 0)
    self.create_arco.connect("clicked", self.on_create_arco_clicked)

    hbox0.pack_start(lbl_create_arco, False, False, 0)
    hbox0.pack_start(self.iso_choices, False, False, 0)
    hbox0.pack_end(self.create_arco, False, False, 0)
    hbox0.pack_end(self.enable_hold, False, False, 0)

    # ======================================================================
    #                           HBOX 1
    # ======================================================================

    lbl_create_arch = Gtk.Label(label="Create your personal Arch Linux iso: ")
    self.create_arch = Gtk.Button(label="Create")
    self.create_arch.set_size_request(280, 0)
    self.create_arch.connect("clicked", self.on_create_arch_clicked)

    hbox1.pack_start(lbl_create_arch, False, False, 0)
    hbox1.pack_end(self.create_arch, False, False, 0)

    # ======================================================================
    #                           HBOX 5
    # ======================================================================

    lbl_clean_pacman_cache = Gtk.Label(label="Clean the pacman cache: ")
    self.clean_pacman_cache = Gtk.Button(label="Clean")
    self.clean_pacman_cache.set_size_request(280, 0)
    self.clean_pacman_cache.connect("clicked", self.on_clean_pacman_cache_clicked)

    hbox5.pack_start(lbl_clean_pacman_cache, False, False, 0)
    hbox5.pack_end(self.clean_pacman_cache, False, False, 0)

    # ======================================================================
    #                           HBOX 6
    # ======================================================================

    lbl_get_nemesis = Gtk.Label(label="Get the ArcoLinux nemesis scripts: ")
    self.get_nemesis = Gtk.Button(label="Install them")
    self.get_nemesis.set_size_request(280, 0)
    self.get_nemesis.connect("clicked", self.on_get_nemesis_clicked)

    hbox6.pack_start(lbl_get_nemesis, False, False, 0)
    hbox6.pack_end(self.get_nemesis, False, False, 0)

    # ======================================================================
    #                           HBOX 2
    # ======================================================================

    lbl_fix_arch = Gtk.Label(label="Fix keys: ")
    self.fix_arch = Gtk.Button(label="Fix")
    self.fix_arch.set_size_request(280, 0)
    self.fix_arch.connect("clicked", self.on_fix_arch_clicked)

    hbox2.pack_start(lbl_fix_arch, False, False, 0)
    hbox2.pack_end(self.fix_arch, False, False, 0)

    # ======================================================================
    #                           HBOX 9
    # ======================================================================

    lbl_probe = Gtk.Label(label="Provide probe link: ")
    self.probe = Gtk.Button(label="Get probe link")
    self.probe.set_size_request(280, 0)
    self.probe.connect("clicked", self.on_probe_clicked)

    hbox9.pack_start(lbl_probe, False, False, 0)
    hbox9.pack_end(self.probe, False, False, 0)

    # ======================================================================
    #                           HBOX 3
    # ======================================================================

    lbl_arch_server = Gtk.Label(label="Best Arch Servers: ")
    self.arch_server = Gtk.Button(label="Apply best servers")
    self.arch_server.set_size_request(280, 0)
    self.arch_server.connect("clicked", self.on_arch_server_clicked)

    hbox3.pack_start(lbl_arch_server, False, False, 0)
    hbox3.pack_end(self.arch_server, False, False, 0)

    # ======================================================================
    #                           HBOX 4
    # ======================================================================

    lbl_arco_key_mirror = Gtk.Label(label="Install ArcoLinux Keys and Mirrorlist: ")

    self.arco_key_mirror_install = Gtk.Button(label="Install")
    self.arco_key_mirror_install.set_size_request(280, 0)
    self.arco_key_mirror_install.connect(
        "clicked", self.on_arco_key_mirror_clicked_install
    )

    self.arco_key_mirror_remove = Gtk.Button(label="Remove")
    self.arco_key_mirror_remove.set_size_request(280, 0)
    self.arco_key_mirror_remove.connect(
        "clicked", self.on_arco_key_mirror_clicked_remove
    )

    hbox4.pack_start(lbl_arco_key_mirror, False, False, 0)
    hbox4.pack_end(self.arco_key_mirror_remove, False, False, 0)
    hbox4.pack_end(self.arco_key_mirror_install, False, False, 0)

    # ======================================================================
    #                           HBOX 7
    # ======================================================================

    lbl_pacman_reset = Gtk.Label(label="Reset your /etc/pacman.conf: ")
    self.pacman_reset_local = Gtk.Button(label="From local file")
    self.pacman_reset_local.set_size_request(280, 0)
    self.pacman_reset_local.connect("clicked", self.on_pacman_reset_local_clicked)
    self.pacman_reset_cached = Gtk.Button(label="Cached")
    self.pacman_reset_cached.set_size_request(280, 0)
    self.pacman_reset_cached.connect("clicked", self.on_pacman_reset_cached_clicked)

    hbox7.pack_start(lbl_pacman_reset, False, False, 0)
    hbox7.pack_end(self.pacman_reset_local, False, False, 0)
    hbox7.pack_end(self.pacman_reset_cached, False, False, 0)

    # ======================================================================
    #                           HBOX 8
    # ======================================================================

    lbl_packages_installer = Gtk.Label(label="Install packages from file: ")
    self.packages_path = Gtk.Entry()
    btnsearch = Gtk.Button(label=". . .")
    btnsearch.connect("clicked", self.on_find_path)
    btninstall = Gtk.Button(label="Install")
    btninstall.connect("clicked", self.on_pacman_install_packages)
    hbox8.pack_start(lbl_packages_installer, False, False, 0)
    hbox8.pack_start(self.packages_path, True, True, 0)
    hbox8.pack_end(btninstall, False, False, 0)
    hbox8.pack_end(btnsearch, False, False, 0)

    # # ======================================================================
    # #                            Message
    # # ======================================================================

    lblmessage = Gtk.Label()
    lblmessage.set_justify(Gtk.Justification.CENTER)
    lblmessage.set_line_wrap(True)
    lblmessage.set_markup(
        '<span foreground="white" size="x-large">Use the hold option to keep Alacritty open and analyze. \n \
Do not use it to build an ISO!</span>'
    )
    # if self.enable_hold.get_active():
    hbox_message.pack_start(lblmessage, True, False, 0)
    # ======================================================================
    #                       HBOX_BUTTONS
    # ======================================================================

    btnClose = Gtk.Button(label="Close")
    btnClose.connect("clicked", self.on_close_clicked)
    # btnSave = Gtk.Button(label="Save")
    # btnSave.connect("clicked", self.on_save_clicked)

    hbox_buttons.pack_end(btnClose, False, False, 0)
    # hbox_buttons.pack_end(btnSave, False, False, 0)

    # ======================================================================
    #                   PACK TO WINDOW
    # ======================================================================

    scrolledWindow = Gtk.ScrolledWindow()
    self.add(scrolledWindow)

    vbox.pack_start(hbox_revealer, False, False, 20)  # LOGO
    vbox.pack_start(hbox_logo, False, False, 20)  # LOGO
    vbox.pack_start(hbox0, False, False, 0)
    vbox.pack_start(hbox1, False, False, 0)
    vbox.pack_start(hbox5, False, False, 0)
    vbox.pack_start(hbox6, False, False, 0)
    vbox.pack_start(hbox2, False, False, 0)
    vbox.pack_start(hbox9, False, False, 0)
    vbox.pack_start(hbox3, False, False, 0)
    vbox.pack_start(hbox4, False, False, 0)
    vbox.pack_start(hbox7, False, False, 0)
    vbox.pack_start(hbox8, False, False, 0)
    vbox.pack_end(hbox_buttons, False, False, 7)  # Buttons
    vbox.pack_end(hbox_message, False, False, 7)  # Message

    scrolledWindow.add(vbox)
