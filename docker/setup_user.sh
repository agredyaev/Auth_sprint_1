#!/bin/sh
# Parameters:
# $1 - Group ID
# $2 - User ID
# $3 - Username and group
set -e
set -x

addgroup -g "$1" "$3"
adduser -D -h /opt/app -u "$2" -G "$3" "$3"
chown -R "$3":"$3" /opt/app
