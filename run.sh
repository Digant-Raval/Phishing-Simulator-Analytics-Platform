#!/bin/bash

# Kill any previous Flask/ngrok processes to avoid duplicates
pkill -f "python app.py"
pkill -f "ngrok"

# Trap CTRL+C so both Flask and ngrok stop together
trap "pkill -f 'python app.py'; pkill -f 'ngrok'; exit" INT

# Start Flask in the background
python app.py &

# Give Flask a few seconds to start
sleep 3

# Start ngrok in the background
ngrok http 5000 > /dev/null &

# Give ngrok a second to spin up
sleep 2

# Fetch the public URL from ngrok's local API
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | grep -o "https://[a-zA-Z0-9.-]*.ngrok-free.app" | head -n 1)

# Print out the phishing links
echo "====================================="
echo "✅ Ngrok tunnel started: $NGROK_URL"
echo "📩 Send email: $NGROK_URL/send_email"
echo "🎯 Phishing link: $NGROK_URL/track"
echo "📊 Dashboard: $NGROK_URL/clicks"
echo "====================================="

# Keep script running so ngrok stays alive
wait

