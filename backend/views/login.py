from flask import Flask, request, url_for, Blueprint, render_template, session, redirect, jsonify
from db_model import db_manager
import os
 
users = db_manager.fetch_all("SELECT * FROM User")
print("this are the users for login: ", users)
 
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
        #password = request.form.get('password')
 
        # Check if the user exists and the password matches
        for user in users:
            if email in user and password in user:
                session['user_id'] = 1
                session['user_name'] = "test"
                session['user_email'] = email
                return redirect(url_for('main_page'))
        
            else:
                return jsonify({
                "message": "Invalid email or password"
            }), 401
    else:
        # Render the login form
        return render_template('login.html')