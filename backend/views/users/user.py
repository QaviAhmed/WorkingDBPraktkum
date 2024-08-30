from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from db_model import db_manager
from collections import namedtuple
import base64


# Load actual image files and convert them to base64
def load_image_as_base64(image_path):
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

profile_pics = [
    {'id' :1, 'data': load_image_as_base64('backend/static/profiles_pics/pic1.jpg')},
    {'id': 2, 'data': load_image_as_base64('backend/static/profiles_pics/pic2.jpg')},
    {'id':3, 'data': load_image_as_base64('backend/static/profiles_pics/pic3.jpg')},
    {'id':4, 'data': load_image_as_base64('backend/static/profiles_pics/pic4.jpg')},
    {'id':5, 'data': load_image_as_base64('backend/static/profiles_pics/pic5.jpg')}
]
user_manage_page = Blueprint('user_manage_page', __name__, template_folder="frontend/templates/User")

@user_manage_page.route('/account/<int:user_id>', methods=['GET', 'POST'])
def manage_account(user_id):
    user_data = db_manager.fetch_one("SELECT user_id, name, birthdate, email, role, address_id FROM Users WHERE user_id=%s", user_id)
    User = namedtuple('User', ['user_id', 'name', 'birthdate', 'email', 'role', 'address_id'])
    user_serialized = User(*user_data)._asdict()
    address_data = db_manager.fetch_one('SELECT street, house_number, postal_code, city, country FROM Address WHERE address_id = %s', user_serialized['address_id'])
    print(address_data)
    Address = namedtuple('Address', ['street', 'house_number', 'postal_code', 'city', 'country'])
    address_serialized = Address(*address_data)._asdict()
    print(user_data)
    if request.method == 'POST':
        user_name = request.form.get('name')
        user_birthdate = request.form.get('birthdate')
        user_address = request.form.get('address')
        user_profile_image = int(request.form.get('profile_pic_id'))
        db_manager.execute_query("""UPDATE Users SET name = %s, birthdate = %s, address_id = %s, profile_image = %s""", (user_name, user_birthdate, \
                                                                                                                         user_address, profile_pics[str(user_profile_image)]))
        
        flash('Account details updated successfully!', 'success')
        return redirect(url_for('manage_account', user_id=user_id))
    return render_template('manage_account.html', user=user_serialized, profile_pics=profile_pics, address=address_serialized)