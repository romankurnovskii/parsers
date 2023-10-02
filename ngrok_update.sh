#!/bin/bash
ngrok tcp 22 >/dev/null &
sleep 10
export WEBHOOK_URL="$(curl http://localhost:4040/api/tunnels | jq ".tunnels[0].public_url")"
curl "https://script.google.com/macros/s/AKfycbxlZ5OxzdXi3l2D4THE4NOmSilEMYLp_Upsf9Rk55WdAm40tEENkyzygEZ1lODeVWdN/exec?WEBHOOK_URL=$WEBHOOK_URL" &
