#!/usr/bin/env bash

if [ $UID != 0 ]; then
    echo 'pls run as root!'
    exit 1
fi

GAME_SERVER_HOME=/opt/game-server

rm -vrf /opt/game-server
mkdir -p /opt/game-server
cp -rv * /opt/game-server

mkdir -p /var/log/game-server
python -m venv $GAME_SERVER_HOME/env
$GAME_SERVER_HOME/env/bin/python -m pip install -r requirements.txt

cp -v /opt/game-server/game-server.service /etc/systemd/system
systemctl enable --now game-server.service

echo install done
