#!/usr/bin/env bash

set -euo pipefail
echo "# Loading VirtualEnvironment"
. /home/pi/.local/share/virtualenvs/nj-unemployment-notifier-_Z7Yr6Xu/bin/activate;
echo "# Running main script"
python /home/pi/nj-unemployment-notifier/main.py;
echo "# Main script successful"
