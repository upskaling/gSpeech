{ lib
, python3
, gtk3
, wrapGAppsHook
, glibcLocales
, gobject-introspection
, gettext
, pango
, gdk-pixbuf
, atk
, libnotify
, libappindicator-gtk3
, gst_all_1
}:

python3.pkgs.buildPythonApplication rec {
  pname = "gspeech";
  version = "0.9.0";

  src = lib.cleanSource ./.;

  nativeBuildInputs = [
    wrapGAppsHook
    gobject-introspection
    pango
    gdk-pixbuf
    atk
    gettext
    glibcLocales
    libnotify
    libappindicator-gtk3
    gst_all_1.gstreamer
    gst_all_1.gst-plugins-base
    gst_all_1.gst-plugins-good
  ];

  buildInputs = [
    gtk3
    python3
  ];

  makeWrapperArgs = [
    "--set LOCALE_ARCHIVE ${glibcLocales}/lib/locale/locale-archive"
    "--set CHARSET en_us.UTF-8"
  ];

  propagatedBuildInputs = with python3.pkgs; [
    pygobject3
  ];

  meta = with lib; {
    description = "A GUI for the Text To Speech Svoxpico.";
    homepage = "https://github.com/mothsART/gspeech";
    maintainers = with maintainers; [ "mothsart" ];
    license = licenses.gpl3;
    platforms = platforms.unix;
  };
}
