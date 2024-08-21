from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

with open('/Users/eduardgol/Desktop/OurProject/WorkingDBPraktkum/backend/views/users.json', 'r') as file:
    data = json.load(file)

users = data['users_data']

template_dir = os.path.abspath("/Users/eduardgol/Desktop/OurProject/WorkingDBPraktkum/frontend/templates")
app = Flask(__name__, template_folder=template_dir)


@app.route('/registration', methods=['POST'])
def registration():
    data = request.get_json()
    print(data)
    name = data.get("name")
    
    # password = data.get('password')
 
    # Check if the user exists and the password matches
    for user in users:
        if user["email"] != data.get("email"):
            return jsonify({
            "message": "Registration successful",
        }), 200
        else:
            return render_template('falschRegister.html')
        
    
"""@app.route('/login', methods=['GET'])
def login_get():
    return json.dumps({"status": "success", "data": {"key": "Hello, world"}})
   """
if __name__ == '__main__':
    app.run(debug=True)
