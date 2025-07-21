from flask import Flask, render_template, jsonify
from datetime import datetime
import subprocess

app = Flask(__name__)

status_log = {
    "last_run": None,
    "current_task": "Idle",
    "auto_mode": False
}

@app.route('/')
def index():
    return render_template('index.html', status=status_log)

@app.route('/start')
def start_generation():
    status_log["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_log["current_task"] = "Running full pipeline..."

    # This runs the entire ebook pipeline in the background
    subprocess.Popen(["python", "../scripts/scheduler.py"])

    return jsonify({"message": "Pipeline started!"})

@app.route('/status')
def get_status():
    return jsonify(status_log)

@app.route('/toggle-auto')
def toggle_auto():
    status_log["auto_mode"] = not status_log["auto_mode"]
    return jsonify({"auto_mode": status_log["auto_mode"]})

if __name__ == "__main__":
    app.run(debug=True)
