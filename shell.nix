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
    mesa
  ];

  # Shell hook to set up environment
  shellHook = ''
    export TMPDIR=/tmp
    export UV_PYTHON="${python}/bin/python"
    export MUJOCO_GL=egl
    export PYOPENGL_PLATFORM=egl
    unset MUJOCO_EGL_DEVICE_ID
    export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.mesa}/lib:$LD_LIBRARY_PATH"
    just install
  '';
}
