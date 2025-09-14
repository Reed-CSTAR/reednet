{
  description = "The Nix config for Polytopia";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  };

  outputs =
    inputs@{ self, nixpkgs, ... }:
    let
      allSystems = nixpkgs.lib.systems.flakeExposed;
      forAllSystems = nixpkgs.lib.genAttrs allSystems;
      define =
        f:
        forAllSystems (
          system:
          let
            pkgs = import nixpkgs {
              inherit system;
              config = {
                allowUnfree = true;
              };
            };
          in
          f pkgs
        );
    in
    {
      devShells = define (
        pkgs:
        let
          inherit (pkgs.lib)
            mapAttrs'
            nameValuePair
            removeSuffix

            getExe
            getExe'
            ;
        in
        {
          default = pkgs.mkShell {
            buildInputs = [
              pkgs.ansible
              pkgs.dhall
              pkgs.mkpasswd
              pkgs.sshpass
              (pkgs.writeShellScriptBin "poly-run-ansible" ''
                exec ${getExe' pkgs.ansible "ansible-playbook"} -i inventory.yaml playbook.yaml -K -k -u polytopia "$@"
              '')
              (pkgs.writeShellScriptBin "poly-ping" ''
                exec ${getExe' pkgs.ansible "ansible"} all -m ping -i inventory.yaml -k -v -u polytopia
              '')
              (pkgs.writeShellScriptBin "poly-hash-password" ''
                exec ${getExe pkgs.mkpasswd} --method=yescrypt "$@"
              '')
            ];
            shellHook = ''
              if ! [[ "$(id -u -n)" =~ ^(sam|a?tali)$ ]]; then
                cat <<< "This dev shell is meant for administration of CS department computers.
              You likely ran something along the lines of

                  nix develop polytopia

              This is probably not what you meant to run.
              Did you mean something like the following?

                  nix develop polytopia#cs221

              If you know what you're doing, feel free to ignore this message."
              fi
            '';
          };
        }
        // mapAttrs' (
          name: _: nameValuePair (removeSuffix ".nix" name) (pkgs.callPackage (./devShells + "/${name}") { })
        ) (builtins.readDir ./devShells)
      );

      formatter = define (pkgs: pkgs.nixfmt);
    };
}
