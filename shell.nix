let
  nixpkgs = fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/tarball/nixos-25.05";
    sha256 = "062g9k0dn0x6a7pcc4w17gkv7sd8gnbbsbr8cmihqdpsrs355gmp";
  };
  pkgs = import nixpkgs { config = {allowUnfree=true;}; overlays = []; };
in

let
  shell_packages = with pkgs; [
    git
    jujutsu
    pre-commit
    poetry
  ];
in

pkgs.mkShell {
  buildInputs = shell_packages;

  shellHook = ''
    has_venv_dir=false
    has_pyproject=false

    [ -d ".venv" ] && has_venv_dir=true
    [ -f "pyproject.toml" ] && has_pyproject=true

    if ! $has_venv_dir && $has_pyproject; then
      echo "Creating a virtual environment..."
      poetry config virtualenvs.in-project true --local
      poetry install --with dev
    fi

    if $has_venv_dir; then
      echo "Activating the virtual environment..."
      source .venv/bin/activate
    fi
  '';
}
