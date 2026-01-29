{ config, lib, pkgs, sign-sink, sign-source, ... }:

{
  systemd.services.sign-sink = {
    wantedBy = [ "multi-user.target" ];
    environment.RUST_LOG = "debug";
    serviceConfig.ExecStart = "${sign-sink.packages.x86_64-linux.default}/bin/nextbus-sign-server";
  };

  systemd.services.sign-source = {
    wantedBy = [ "multi-user.target" ];
    wants = [ "sign-sink.service" ];

    serviceConfig.ExecStart = "${sign-source.packages.x86_64-linux.default}/bin/railway-uptime-monitor";
  };
}
