from flask import Flask, render_template
import json
import mariadb
import sys
import os
from test_sql import connecting_mariadb
####################################
#data = {"status": "hello, World2"}
#   return json.dumps(data)


    
template_dir = os.path.abspath("/Users/eduardgol/Desktop/OurProject/WorkingDBPraktkum/frontend/templates")
print(template_dir)
app = Flask(__name__, template_folder=template_dir)
connecting_mariadb()

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)




