# keep_alive.py - Simple Flask server to prevent Replit from sleeping
# Ping this endpoint via UptimeRobot every 5 minutes

from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
