{
  description = "reproducible build for kas-moe-back development environment";

  inputs = {
    stable.url = "github:NixOS/nixpkgs/nixos-20.09";
  };

  outputs = inputs:
    let
      system = "x86_64-linux";
      pkgs = inputs.stable.legacyPackages.${system};
      env = pkgs.poetry2nix.mkPoetryEnv { projectDir = ./.; };
    in {
      devShell."${system}" = pkgs.mkShell {
        buildInputs = with pkgs; [ env
	  cookiecutter
	  openssl
	  postgresql
          python38Packages.poetry
          python38Packages.invoke
          python38Packages.flake8
          python38Packages.flake8-polyfill
          python38Packages.uvicorn
          python38Packages.gunicorn
        ];
      };
    };
}
