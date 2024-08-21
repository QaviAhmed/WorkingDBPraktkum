from flask import Flask, render_template
import json
import sys
import os
from test_sql import connecting_mariadb
    
template_dir = os.path.abspath("/Users/eduardgol/Desktop/OurProject/WorkingDBPraktkum/frontend/templates")
app = Flask(__name__, template_folder=template_dir)
connecting_mariadb()

@app.route("/", methods=['GET'])
def index():
    return render_template('main.html')


if __name__ == "__main__":
    app.run(debug=True)




