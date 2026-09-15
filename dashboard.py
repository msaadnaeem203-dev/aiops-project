from flask import Flask
import subprocess
import sys

app = Flask(__name__)

@app.route("/")
def dashboard():
    result = subprocess.run(
        [sys.executable , "health_summary.py"],
        capture_output=True,
        text=True
    )

    output = result.stdout.strip()

    return f"""
    <html>
    <head>
        <title>AIOps Health Dashboard</title>
        <meta http-equiv="refresh" content="5">
    </head>
    <body>
        <h1>AIOps Health Dashboard</h1>

        <h2>Live Health Summary</h2>

        <pre>{output}</pre>

        <p>Dashboard refreshes every 5 seconds.</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
