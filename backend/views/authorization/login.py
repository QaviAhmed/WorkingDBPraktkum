from flask import Flask, request, url_for, Blueprint, render_template, session, redirect, jsonify
from db_model import db_manager
import os
 
users = db_manager.fetch_all("SELECT * FROM Users")
 
template_dir = os.path.abspath("/Users/qavi/Desktop/SS24/DB_Praktikum/WorkingDBPraktkum/frontend/templates")
login_page = Blueprint('login_page', __name__,
                        template_folder=f"{template_dir}/authorization")
print(template_dir)

@login_page.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process the login form submission
        email = request.form.get('email')
        password = request.form.get('password')
        print("email: ", email, "password: ", password)
        #password = request.form.get('password')
 
        # Check if the user exists and the password matches
        for user in users:
            if email == user[3] and password == user[4]:
                return jsonify({"user_id": user[0], "user_name": user[1], "user_email": email})
        
        error_message = "Invalid email or password"
        return jsonify({"error": error_message})
    # Render the login form for GET requests
    return render_template('login.html')