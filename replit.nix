{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.python311Packages.setuptools
    pkgs.python311Packages.virtualenv
    pkgs.pkg-config
    pkgs.glibcLocales
    pkgs.glib
    pkgs.stdenv.cc.cc
  ];
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.stdenv.cc.cc.lib
      pkgs.glib
    ];
  };
}
