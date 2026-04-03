{
  pkgs ? import <nixpkgs> { },
}:

let
  python = pkgs.python312;
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    python
    uv
    nixfmt
    just
    stdenv.cc.cc.lib
  ];

  # Shell hook to set up environment
  shellHook = ''
    export TMPDIR=/tmp
    export UV_PYTHON="${python}/bin/python"
    export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH"
    just install
  '';
}
