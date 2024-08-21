from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

template_dir = os.path.abspath("/Users/eduardgol/Desktop/OurProject/WorkingDBPraktkum/frontend/templates")


with open('/Users/eduardgol/Desktop/OurProject/WorkingDBPraktkum/backend/views/users.json', 'r') as file:
    data = json.load(file)

users = data['users_data']

app = Flask(__name__, template_folder=template_dir)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        data = request.get_json()
        for user in users:
            if user["email"] != data.get("email"):
                return jsonify({"message": "Registration successful",}), 200
            else:
                return render_template('errorRegistration.html')
    else:
        return render_template('registration.html')
        
        
if __name__ == '__main__':
    app.run(debug=True)
