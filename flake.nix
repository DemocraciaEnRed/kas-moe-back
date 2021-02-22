{
  description = "kas-moe-back development environment reproducible build";

  inputs = {
    stable.url = "github:NixOS/nixpkgs/nixos-20.09";
    unstable.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = inputs:
    let
      system = "x86_64-linux";
      pkgs = inputs.stable.legacyPackages.${system};
      env = pkgs.poetry2nix.mkPoetryEnv { projectDir = ./.; };
    in {
      devShell."${system}" = pkgs.mkShell {
        buildInputs = with pkgs; [
	  env
	  python38Packages.pip
	  python38Packages.invoke
	  python38Packages.flake8
	  python38Packages.flake8-polyfill
        ];
	shellHook = ''
	  export PIP_DISABLE_PIP_VERSION_CHECK=1;
	  pip install radon;
	'';
      };
    };
}
