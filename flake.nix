{
  description = "kas-moe-back development environment reproducible build";

  inputs = {
    unstable.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = inputs:
    let
      system = "x86_64-linux";
      pkgs = inputs.unstable.legacyPackages.${system};
      env = pkgs.poetry2nix.mkPoetryEnv { projectDir = ./.; };
    in {
      devShell."${system}" = pkgs.mkShell {
        buildInputs = with pkgs; [
	  env
	  python38Packages.pip
	  python38Packages.invoke
	  python38Packages.flake8
	];
	shellHook = ''
	  export PIP_DISABLE_PIP_VERSION_CHECK=1;
	  pip install radon;
	'';
      };
    };
}
