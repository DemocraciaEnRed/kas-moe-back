{ pkgs ? import <nixpkgs> {}}:

pkgs.mkShell rec {
  name = "nodejs-12";

  buildInputs = [
    pkgs.nodejs-12_x
    pkgs.nodePackages.yarn
    pkgs.nodePackages.pnpm
  ];

  postShellHook = ''
    export PATH="$PWD/node_modules/.bin/:$PATH"
    alias run='yarn'
  '';
}
