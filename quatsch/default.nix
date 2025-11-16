# Edit this configuration file to define what should be installed on
# your system. Help is available in the configuration.nix(5) man page, on
# https://search.nixos.org/options and in the NixOS manual (`nixos-help`).

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

  environment.systemPackages = with pkgs; [
    curl git neovim borgbackup

    ghostty.terminfo
  ];

  services.openssh.enable = true;
  services.tailscale.enable = true;

  services.prometheus = {
    enable = true;
    exporters.node.enable = true;
  };

  system.stateVersion = "25.05"; # Did you read the comment?
}
