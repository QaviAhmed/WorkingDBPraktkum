from flask import Flask, render_template, request, redirect, url_for, jsonify, Blueprint, abort
from http import HTTPStatus
import os
from db_model import db_manager
import random
 
users = db_manager.fetch_all("SELECT * FROM Users")
addresses = db_manager.fetch_all("SELECT * FROM Address")
template_dir = os.path.abspath("/Users/eduardgol/Desktop/OurProject/WorkingDBPraktkum/frontend/templates")
register_page = Blueprint('register_page',__name__, template_folder=f" {template_dir}/authorization")
 
 
@register_page.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        # user infos
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        birthdate = request.form.get('birthdate')
        role = request.form.get('role')
        user_id = random.randrange(0, 100000)  # Use a better way to generate unique IDs

        # address info
        street = request.form.get('street')
        house_number = request.form.get('house_number')
        postal_code = request.form.get('postel_code')
        city = request.form.get('city')
        country = request.form.get('country')
        tuple_address = (street, house_number, postal_code, city, country)
        print("this is tupled data: ", tuple_address)
        

        # Insert the new address
        query = f"""
            INSERT INTO Address (street, house_number, postal_code, city, country) 
            VALUES ('{street}', '{house_number}', '{postal_code}', '{city}', '{country}')
        """

        # Execute the query
        try:
            db_manager.execute_query(query)
        except Exception as e:
            print(e)

        # Check if the user already exists by email
        user_exists = db_manager.fetch_one("SELECT * FROM Users WHERE email = %s", (email))
        print(user_exists)
        if user_exists != None:
            return abort(409, "User already exists")
        else:
            # Fetch the new address_id
            new_address_id = db_manager.fetch_one("SELECT * FROM Address WHERE street = %s OR house_number = %s OR postal_code = %s", (street, house_number, postal_code))
            print("this is for the new_address_id: ", new_address_id)  # Access the address_id from the tuple
            # Insert the new user with the correct address_id
            db_manager.execute_query(f"""
                INSERT INTO Users (user_id, name, birthdate, email, password, address_id, role) 
                VALUES ('{user_id}', '{name}', '{birthdate}', '{email}', '{password}', '{6}', '{role}')
            """)
    
    return render_template('register.html')

