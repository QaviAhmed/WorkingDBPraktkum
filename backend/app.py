from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route("/")
def index():
    data = {"status": "hello, World"}
    return json.dumps(data)

if __name__ == "__main__":
    app.run(debug=True)
