from flask import Flask, request, jsonify, render_template, Blueprint
from db_model import db_manager
import os
from serialization import Serialization  


users_data = db_manager.fetch_all("SELECT * FROM User")
serialized_users = Serialization(users_data, "User", ['user_ID', 'name', 'city', 'birthday', 'email', 'password']).get_data()
 

template_dir = os.path.abspath("/Users/eduardgol/Desktop/OurProject/WorkingDBPraktkum/frontend/templates")
login_page = Blueprint('login_page',__name__, template_folder=f"{template_dir}/authorization")
 
 
@login_page.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process the login form submission
        email = request.form.get('email')
        #password = request.form.get('password')
        print(email)

        # Check if the user exists and the password matches
        for user in serialized_users:
            print(user)
            if user["email"] == email:
                return jsonify({
                "message": "Login successful",
                "user": user["name"]
            }), 200
       
        else:
            return jsonify({
            "message": "Invalid email or password"
            }), 401
    else:
        # Render the login form
        return render_template('login.html')
    