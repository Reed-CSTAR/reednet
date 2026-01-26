{ config, lib, pkgs, ... }:

{
  imports =
    [ # Include the results of the hardware scan.
      ./hardware-configuration.nix
    ];

  # Use the systemd-boot EFI boot loader.
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;

  networking.hostName = "quatsch";
  networking.networkmanager.enable = true;

  networking.interfaces.enp0s6f1u2.ipv4.addresses = [
    {
      address = "10.114.102.2";
      prefixLength = 24;
    }
  ];

  nix.settings."experimental-features" = [ "nix-command" "flakes" ];

  time.timeZone = "America/Los_Angeles";

  users.users = {
    polytopia = {
      isNormalUser = true;
      extraGroups = [ "wheel" ];

      openssh.authorizedKeys.keys = [
        "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHlsdZRN8i12v5Uv2ZZtGqxqbf8T/n0H6U/UagIPUZy5 tali@thing-in-itself"
      ];
    };

    backups = {
      isNormalUser = true;

      openssh.authorizedKeys.keys = [
        "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIH6mCbSIO2ryykiSGoHknxi+Bs3UAaCoJVao4IKNeVAb root@patty"
        "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEH5XuWSd+HLrit6ckDHOcn1gEV5SBnMoRekPDMBYyLQ root@polly"
      ];
    };
  };

  environment.variables = rec {
    EDITOR = "nvim";
    VISUAL = EDITOR;
  };

  environment.systemPackages = with pkgs; [
    curl git neovim borgbackup

    ghostty.terminfo
  ];

  services.openssh.enable = true;
  services.tailscale.enable = true;

  services.prometheus = {
    enable = true;
    exporters.node.enable = true;

    scrapeConfigs = [{
      job_name = "scrape_jobs";
      static_configs = [{
        targets = [
          "localhost:9100"
          "patty.reed.edu"
          "peggy.reed.edu"
          "polly.reed.edu"
          "banku.reed.edu"
          "empanada.reed.edu"
          "gyoza.reed.edu"
          "pierogi.reed.edu"
        ];
      }];
    }];
  };

  security.pki.certificateFiles = builtins.filter
    (lib.hasSuffix ".cert") (lib.filesystem.listFilesRecursive ../certs);

  system.stateVersion = "25.05"; # Did you read the comment?
}
