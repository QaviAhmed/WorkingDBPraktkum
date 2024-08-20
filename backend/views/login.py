from flask import Flask, request, jsonify
import json

with open('/Users/eduardgol/Desktop/OurProject/WorkingDBPraktkum/backend/views/users.json', 'r') as file:
    data = json.load(file)

users = data['users_data']
 
app = Flask(__name__)
 
 
@app.route('/login', methods=['POST'])
def login():
    # Parse JSON data from the request
    #data = request.get_json()
    # Extract email and password from the JSON data
    email = 'johndoe@example.com'
    password = 'password'
 
    # Check if the user exists and the password matches
    if email in users and users[email]['password'] == password:
        return jsonify({
            "message": "Login successful",
            "user": users[email]['name']
        }), 200
    else:
        return jsonify({
            "message": "Invalid email or password"
        }), 401
   
if __name__ == '__main__':
    app.run(debug=True)