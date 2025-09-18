🎣 PhishTracker – Phishing Simulation & Analytics Platform

PhishTracker is a phishing simulation platform built for security awareness and demonstration purposes. It allows you to send simulated phishing emails, track clicks in real-time, and analyze results in a web-based dashboard. The goal is to educate users on phishing risks and showcase how attackers operate, while giving defenders a safe environment to test and train.

✨ Features

📩 Send phishing emails with multiple pre-built templates (password reset, delivery updates, bank alerts).

🎯 Click tracking with detailed logging of IP, device type, operating system, and browser.

🌍 Geolocation support — logs city, region, and country for each click.

📊 Interactive dashboard with summary stats and a searchable click table.

⬇️ Data export to CSV for offline analysis.

🛠️ Tech Stack

Flask – backend framework

SQLite + SQLAlchemy – database & ORM

Flask-Mail (SMTP) – email sending

Ngrok – secure tunnel for public testing

Bootstrap – responsive dashboard UI

Requests & ipinfo.io API – geolocation lookup

python-user-agents – device, OS, and browser detection
