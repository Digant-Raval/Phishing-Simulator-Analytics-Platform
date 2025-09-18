import os
import io
import csv
import requests
from datetime import datetime
from flask import Flask, request, Response, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from dotenv import load_dotenv
from user_agents import parse

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clicks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

db = SQLAlchemy(app)
mail = Mail(app)

# Database model
class Click(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50))
    user_agent = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    city = db.Column(db.String(100))
    region = db.Column(db.String(100))
    country = db.Column(db.String(10))

# Helper: get recipients from file
def get_recipients():
    if os.path.exists("recipients.txt"):
        with open("recipients.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    return [os.getenv("MAIL_USERNAME")]  # fallback to self

# Helper: get ngrok URL
def get_public_url():
    try:
        res = requests.get("http://127.0.0.1:4040/api/tunnels").json()
        for tunnel in res.get("tunnels", []):
            if tunnel["public_url"].startswith("https://"):
                return tunnel["public_url"]
    except Exception as e:
        print("⚠️ Could not fetch ngrok URL:", e)
    return os.getenv("BASE_URL", "http://127.0.0.1:5000")

# Templates
templates = {
    "password_reset": {
        "subject": "Password Reset Required!",
        "body": "Click the link to reset your password: {BASE_URL}/track"
    },
    "package_delivery": {
        "subject": "📦 Your Package Delivery Update",
        "body": "Track your package here: {BASE_URL}/track"
    },
    "bank_alert": {
        "subject": "⚠️ Suspicious Login Attempt",
        "body": "Verify your account immediately: {BASE_URL}/track"
    }
}

# Route: track clicks
@app.route("/track")
def track():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent", "Unknown")

    city, region, country = "Unknown", "Unknown", "Unknown"
    try:
        res = requests.get(f"https://ipinfo.io/{ip}/json").json()
        city = res.get("city", "Unknown")
        region = res.get("region", "Unknown")
        country = res.get("country", "Unknown")
    except Exception as e:
        print("⚠️ Geolocation lookup failed:", e)

    click = Click(ip=ip, user_agent=ua, city=city, region=region, country=country)
    db.session.add(click)
    db.session.commit()

    return "<h2>✅ Thank you. Your request has been processed.</h2>"

# Route: clicks dashboard
@app.route("/clicks")
def show_clicks():
    all_clicks = Click.query.all()
    total_clicks = len(all_clicks)
    unique_ips = len(set(c.ip for c in all_clicks))

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Phishing Clicks</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container mt-5">
            <h1 class="mb-4 text-center">📊 Phishing Clicks Dashboard</h1>

            <div class="row mb-4 text-center">
                <div class="col-md-6">
                    <div class="card shadow-sm border-primary">
                        <div class="card-body">
                            <h5 class="card-title">Total Clicks</h5>
                            <p class="card-text fs-3 fw-bold text-primary">{total_clicks}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card shadow-sm border-success">
                        <div class="card-body">
                            <h5 class="card-title">Unique IPs</h5>
                            <p class="card-text fs-3 fw-bold text-success">{unique_ips}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="mb-3 text-end">
                <a href="/download_csv" class="btn btn-sm btn-outline-primary">⬇️ Download CSV</a>
            </div>

            <table class="table table-striped table-bordered table-hover shadow-sm">
                <thead class="table-dark">
                    <tr>
                        <th>ID</th>
                        <th>IP Address</th>
                        <th>Device</th>
                        <th>OS</th>
                        <th>Browser</th>
                        <th>City</th>
                        <th>Region</th>
                        <th>Country</th>
                        <th>Timestamp</th>
                    </tr>
                </thead>
                <tbody>
    """

    for c in all_clicks:
        ua = parse(c.user_agent or "")
        device = "Mobile" if ua.is_mobile else "Tablet" if ua.is_tablet else "PC"
        os_name = ua.os.family
        browser = ua.browser.family

        html += f"""
            <tr>
                <td>{c.id}</td>
                <td>{c.ip}</td>
                <td>{device}</td>
                <td>{os_name}</td>
                <td>{browser}</td>
                <td>{c.city or 'Unknown'}</td>
                <td>{c.region or 'Unknown'}</td>
                <td>{c.country or 'Unknown'}</td>
                <td>{c.timestamp}</td>
            </tr>
        """

    html += """
                </tbody>
            </table>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    return html

# Route: CSV download
@app.route("/download_csv")
def download_csv():
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["ID", "IP Address", "User Agent", "City", "Region", "Country", "Timestamp"])
    clicks = Click.query.all()
    for c in clicks:
        writer.writerow([c.id, c.ip, c.user_agent, c.city, c.region, c.country, c.timestamp])

    output.seek(0)
    return Response(output.getvalue(),
                    mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=clicks.csv"})

# Route: send email
@app.route("/send_email", methods=["GET", "POST"])
def send_email():
    if request.method == "POST":
        template_choice = request.form["template"]
        template = templates[template_choice]
        base_url = get_public_url()

        msg = Message(
            subject=template["subject"],
            sender=app.config["MAIL_USERNAME"],
            recipients=get_recipients()
        )
        msg.body = template["body"].format(BASE_URL=base_url)
        mail.send(msg)
        return f"✅ Email sent using template: {template_choice}"

    html_form = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Send Phishing Email</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container mt-5">
            <h1 class="mb-4">✉️ Send Phishing Email</h1>
            <form method="post">
                <label for="template">Choose Template:</label>
                <select name="template" id="template" class="form-select mb-3">
                    <option value="password_reset">Password Reset</option>
                    <option value="package_delivery">Package Delivery</option>
                    <option value="bank_alert">Bank Alert</option>
                </select>
                <button type="submit" class="btn btn-primary">Send Email</button>
            </form>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_form)

# Init DB function
def init_db():
    with app.app_context():
        db.create_all()
        print("✅ Database and tables created!")

if __name__ == "__main__":
    # Only run DB init in actual serving process (not reloader parent)
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        init_db()

    app.run(debug=True, use_reloader=True)

