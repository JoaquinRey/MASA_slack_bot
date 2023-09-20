from flask import Flask

app = Flask(__name__)

@app.route("/")
def is_online():
    return "<p>Slack bot is online</p>"

app.run(debug=True, port=3000)