from flask import Flask, request, jsonify, render_template
import json, os

template_dir = os.path.abspath("/Users/eduardgol/Desktop/OurProject/WorkingDBPraktkum/frontend/templates")

#get users data from database
with open('/Users/eduardgol/Desktop/OurProject/WorkingDBPraktkum/backend/views/users.json', 'r') as file:
    data = json.load(file)
users = data['users_data']
 
app = Flask(__name__, template_folder=template_dir)
 
 
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get("email")
 
        # Check if the user exists and the password matches
        for user in users:
            if user["email"] == email:
                return jsonify({"message": "Login successful","user": user["name"]}), 200
        
            else:
                return jsonify({"message": "Invalid email or password"}), 401
    else:
        return render_template('login.html')

    
        
if __name__ == '__main__':
    app.run(debug=True)
