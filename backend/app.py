from flask import Flask, render_template, session, redirect, url_for, jsonify
import json
import sys
import os
from db_model import db_manager
from views.products.products import products_page, product_detail_page
from views.authorization.login import login_page
from views.authorization.registration import register_page
    
template_dir = os.path.abspath("/Users/qavi/Desktop/OurProject/WorkingDBPraktkum/frontend/templates")
app = Flask(__name__, template_folder=template_dir)
app.register_blueprint(products_page)
app.register_blueprint(login_page)
app.register_blueprint(register_page)
app.register_blueprint(product_detail_page)

# -- sessions setup --
app.secret_key = 'supersecretkey'
app.config.update(
    SESSION_COOKIE_NAME="logged_in",
    SESSION_COOKIE_SECURE=False,   # Set to True if using HTTPS
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax", # Options: 'Strict', 'Lax', or 'None'
    SESSION_PERMANENT=False        # Set to True for permanent sessions
)
@app.route('/')
def main_page():
    print("this are the sessions: ", session.get("user_name"))
    if 'user_id' in session:
        user_details = {"name": session['user_name'], "email": session['user_email']}
        print(user_details)
        return render_template('index.html', user=user_details)
    else:
        return jsonify({"status": "failure"})

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)




