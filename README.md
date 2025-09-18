<h1 align="center">🎣 PhishTracker</h1>
<h3 align="center">Phishing Simulation & Awareness Tool</h3>

---

## 📖 Overview
PhishTracker is a phishing simulation platform built for **security awareness and demonstration purposes**.  
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

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/phishtracker.git
cd phishtracker
