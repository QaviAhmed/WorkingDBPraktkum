from flask import Flask, request, jsonify
import json
 
with open('/Users/leona/OneDrive/Desktop/DBP/WorkingDBPraktkum/backend/views/users.json', 'r') as file:
    data = json.load(file)
 
users = data['users_data']
print(users)
 
app = Flask(__name__)
 
 
@app.route('/login', methods=['POST'])
def login():
    # Parse JSON data from the request
    data = request.get_json()
    print(data)
    # Extract email 8and password from the JSON data
    email = data.get("email")
    
    # password = data.get('password')
 
    # Check if the user exists and the password matches
    for user in users:
        if user["email"] == email:
            return jsonify({
            "message": "Login successful",
            "user": user["name"]
        }), 200
        
        else:
            return jsonify({
            "message": "Invalid email or password"
        }), 401
        
    
"""@app.route('/login', methods=['GET'])
def login_get():
    return json.dumps({"status": "success", "data": {"key": "Hello, world"}})
   """
if __name__ == '__main__':
    app.run(debug=True)