#!/bin/bash

# 1. Install required tools
echo "Installing necessary tools..."
brew install ngrok sleepwatcher jq

# 2. Create the ngrok_wakeup.sh script
SCRIPT_PATH="$HOME/ngrok_wakeup.sh"

cat <<EOL >"$SCRIPT_PATH"
#!/bin/bash
ngrok tcp 22 > /dev/null &
sleep 10
export WEBHOOK_URL="\$(curl http://localhost:4040/api/tunnels | jq ".tunnels[0].public_url")"
curl "https://script.google.com/macros/s/AKfycbxlZ5OxzdXi3l2D4THE4NOmSilEMYLp_Upsf9Rk55WdAm40tEENkyzygEZ1lODeVWdN/exec?WEBHOOK_URL=\$WEBHOOK_URL" &
EOL

chmod +x "$SCRIPT_PATH"

# 3. Create an Automator application
APP_NAME="NgrokAtLogin"
AUTOMATOR_APP="$HOME/Applications/$APP_NAME.app"

echo "Creating Automator Application..."
AUTOMATOR_SCRIPT="
on run
    do shell script \"$SCRIPT_PATH\"
end run
"
echo "$AUTOMATOR_SCRIPT" >/tmp/temp_applescript.scpt
osacompile -o "$AUTOMATOR_APP" /tmp/temp_applescript.scpt
rm /tmp/temp_applescript.scpt

# 4. Add the Automator application to Login Items
echo "Adding to Login Items..."
osascript -e "tell application \"System Events\" to make new login item at end with properties {path:\"$AUTOMATOR_APP\", hidden:false}"

echo "Setup completed!"
