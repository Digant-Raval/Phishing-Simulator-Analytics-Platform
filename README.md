<h1 align="center">🎣 PhishBait</h1>
<h3 align="center">Phishing Simulation & Analytics Platform</h3>

---

## 📖 Overview
PhishBait is a phishing simulation platform built for **security awareness and demonstration purposes**.  
It allows you to send simulated phishing emails, track clicks in real-time, and analyze results in a clean dashboard.  
The goal is to **educate users on phishing risks** while providing a safe environment for testing and training.  

---

## ✨ Features
- 📩 **Send phishing emails** with multiple pre-built templates (password reset, delivery updates, bank alerts).  
- 🎯 **Click tracking** with detailed logging of IP, device type, operating system, and browser.  
- 🌍 **Geolocation support** — logs city, region, and country for each click.  
- 📊 **Interactive dashboard** with summary stats and a searchable click table.  
- ⬇️ **Data export** to CSV for offline analysis.  

---

## 🛠️ Tech Stack
- **Flask** – backend framework  
- **SQLite + SQLAlchemy** – database & ORM  
- **Flask-Mail (SMTP)** – email sending  
- **Ngrok** – secure tunnel for public testing  
- **Bootstrap** – responsive dashboard UI  
- **Requests + ipinfo.io API** – geolocation lookup  
- **python-user-agents** – device, OS, and browser detection  

---
## 🚀 Getting Started

## 🚀 How to Run

```bash
# 1. Clone the repository
git clone https://github.com/Digant-Raval/Phishing-Simulator-Analytics-Platform.git
cd phishtracker

# 2. Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# 3. Install dependencies
pip install -r requirements.txt

# (requirements.txt should contain:)
# Flask==3.0.3
# Flask-SQLAlchemy==3.1.1
# Flask-Mail==0.9.1
# python-dotenv==1.0.1
# requests==2.32.3
# user-agents==2.2.0

# 4. Create a .env file in the project root with your email config:
echo "MAIL_USERNAME=youremail@gmail.com" >> .env
echo "MAIL_PASSWORD=your_app_password" >> .env
echo "BASE_URL=http://127.0.0.1:5000" >> .env

# 5. Run the app (this also starts ngrok for public testing)
./run.sh

# 6. Open the dashboard, email sender, and tracking links:
# 📩 Send Email:   https://<your-ngrok>.ngrok-free.app/send_email
# 🎯 Phishing Link: https://<your-ngrok>.ngrok-free.app/track
# 📊 Dashboard:    https://<your-ngrok>.ngrok-free.app/clicks
