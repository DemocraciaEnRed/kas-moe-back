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
	  python38Packages.invoke
	];
      };
    };
}
