#!/usr/bin/env bash

if [ $UID != 0 ]; then
    echo 'pls run as root'
    exit 1
fi

systemctl stop game-server.service
rm -vf /etc/systemd/system/game-server.service
rm -vrf /opt/game-server
systemctl daemon-reload

echo uninstall done
