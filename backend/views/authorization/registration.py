from flask import Flask, render_template, request, redirect, url_for, jsonify, Blueprint, abort
from http import HTTPStatus
import os
from db_model import db_manager
import random
 
users = db_manager.fetch_all("SELECT * FROM Users")

template_dir = os.path.abspath("/Users/eduardgol/Desktop/OurProject/WorkingDBPraktkum/frontend/templates")
register_page = Blueprint('register_page',__name__, template_folder=f" {template_dir}/authorization")
 
 
@register_page.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        city = request.form.get('city')
        birthdate = request.form.get('birthdate')
        id = random.randrange(0, 100000)
        print(f"{name}, {email}, {password}, {city}, {city}, {birthdate}, {id}")
        
        for user in users:
            if email in user:
                return abort(409, "User exists already")
        db_manager.execute_query("""INSERT INTO User 
                                (user_ID, name, city, birthdate, email, password) VALUES(%s,%s,%s,%s,%s,%s)
                """, (id, name, city, birthdate, email, password))
        return redirect(url_for('main_page'))        
    return render_template('register.html')