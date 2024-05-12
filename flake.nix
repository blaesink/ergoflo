{
  description = "A python functional framework.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    devenv.url = "github:cachix/devenv";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  nixConfig = {
    extra-trusted-public-keys = "devenv.cachix.org-1:w1cLUi8dv3hnoSPGAuibQv+f9TZLr6cv/Hm9XgU50cw=";
    extra-substituters = "https://devenv.cachix.org";
  };

  outputs = inputs@{ flake-parts, poetry2nix, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [
        inputs.devenv.flakeModule
      ];
      systems = [ "x86_64-linux" "x86_64-darwin" "aarch64-linux" "aarch64-darwin" ];

      perSystem = { config, self', inputs', pkgs, system, ... }: 
        let
          python' = pkgs.python312;
          inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) 
            mkPoetryApplication 
            defaultPoetryOverrides;
          pymaybeApp = mkPoetryApplication { 
            projectDir = ./.;
            python = python';
            overrides = defaultPoetryOverrides.extend (self: super: {
                pytest-watcher = super.poetry.overridePythonAttrs (old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ super.poetry ];
                });
              });
          };
        in
      {
        packages.default = pymaybeApp;

        devenv.shells.default = {
          name = "pymaybe";

          languages.python = {
            enable = true;
            package = python';
            poetry = {
              install.enable = true;
              activate.enable = true;
              enable = true;
            };
          };

          env.PYTHONPATH = "$PYTHONPATH:.";

          # https://devenv.sh/reference/options/
          packages = with pkgs; [ poetry pyright ruff-lsp ];

        };

      };
      flake = {};
    };
}
