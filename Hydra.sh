#!/bin/bash

directory=$(pwd)

osascript <<EOF
tell application "Terminal"
    do script "cd $directory && flask --app main.py run"
end tell
EOF

sleep 1

osascript <<EOF
tell application "Terminal"
    do script "cd $directory && npm start"
end tell
EOF


# Run the Python script after a short delay to allow the previous commands to start
#

python guitest.py
