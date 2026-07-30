from flask import Flask, render_template_string
import os
import datetime

app = Flask(__name__)

LOG_FILE = "monitor.log"

@app.route("/")
def home():

    if not os.path.exists(LOG_FILE):
        return "No log file found. Run monitor.py first."

    with open(LOG_FILE, "r") as f:
        logs = f.readlines()

    recent_logs = logs[-20:][::-1]

    html = "<h1>Monitor Dashboard</h1>"
    html += f"<p>Last updated: {datetime.datetime.now()}</p>"
    html += "<pre>"
    for line in recent_logs:
        html += line
    html += "</pre>"

    return html

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

