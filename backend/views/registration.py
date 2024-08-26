from flask import Flask, render_template, request, redirect, url_for, jsonify, Blueprint
import os
from db_model import db_manager
from serialization import Serialization  



users_data = db_manager.fetch_all("SELECT * FROM User")
serialized_users = Serialization(users_data, "User", ['user_ID', 'name', 'city', 'birthday', 'email', 'password']).get_data()

template_dir = os.path.abspath("/Users/eduardgol/Desktop/OurProject/WorkingDBPraktkum/frontend/templates")
register_page = Blueprint('register_page',__name__, template_folder=f" {template_dir}/authorization")


@register_page.route('/registration', methods=['POST','GET'])
def registration():
    if request.method == 'POST':
        data = request.get_json()
        # password = data.get('password')
    
        for user in serialized_users:
            if user["email"] != data.get("email"):
                return jsonify({
                "message": "Registration successful",
            }), 200
            else:
                return jsonify({
                "message": "Registration scheisse",
            }), 200
    return render_template('register.html')