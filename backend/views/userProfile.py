from flask import Flask, request, jsonify, render_template, Blueprint
from db_model import db_manager
import os

users = db_manager.fetch_all("SELECT * FROM User")

template_dir = os.path.abspath("/Users/eduardgol/Desktop/OurProject/WorkingDBPraktkum/frontend/templates")
user_page = Blueprint('user_page',__name__, template_folder=f" {template_dir}/authorization")

 
@user_page.route('/userProfile/<int:user_id>', methods=['GET', 'POST'])
def getUserProfile(user_id):
    if request.method == 'GET':
        for user in users:
            if user["user_ID"] == user_id:
                 return render_template('myAccount.html', person=user)
        
    else:
        return render_template('home.html')
