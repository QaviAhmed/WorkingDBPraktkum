from flask import Flask, render_template, session, redirect, url_for
import json
import sys
import os
from db_model import db_manager
from views.products import products_page
from views.login import login_page
from views.registration import register_page
    
template_dir = os.path.abspath("/Users/qavi/Desktop/OurProject/WorkingDBPraktkum/frontend/templates/main")
app = Flask(__name__, template_folder=template_dir)
app.register_blueprint(products_page)
app.register_blueprint(login_page)
app.register_blueprint(register_page)
app.secret_key = 'supersecretkey'
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

@app.route('/')
def main_page():
    if 'user_id' in session:
        print("this are the sessions: ", session)
        user_details = {"name": session['user_name'], "email": session['user_email']}
        print(user_details)
        return render_template('index.html', user=user_details)
    else:
        return render_template('index.html', user=None)

if __name__ == "__main__":
    app.run(debug=True)




