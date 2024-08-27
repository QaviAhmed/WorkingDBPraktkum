from flask import Flask, request, jsonify, render_template, Blueprint, abort
from jinja2 import TemplateNotFound
import json
from db_model import db_manager
from serialization import Serialization
import os
 
template_dir = os.path.abspath("/Users/qavi/Desktop/SS24/DB_Praktikum/WorkingDBPraktkum/frontend/templates")

products_page = Blueprint('product_page', __name__,
                        template_folder=f"{template_dir}/main")
print(template_dir)
    
products_data = db_manager.fetch_all("SELECT * FROM Product;")
serialized_data = Serialization(products_data, "Product", ['product_ID', 'description', 'image', 'name', 'price']).get_data()

@products_page.route('/', methods=['GET'])
def products():
    return render_template('index.html', products_data=serialized_data)

    
@products_page.route('/products', methods=['POST'])
def create_products():
    # Parse JSON data from the request
    data = request.get_json()
    # Extract product from the JSON data
    product_ID = data.get("product_ID")
 
    # Check if the products exists 
    for product in products_data:
        if product("product_ID") == product_ID:
            return jsonify({
            "message": "Product already exist",
        }), 400
        
        else:
            return jsonify({
            "message": "Product added sucsessful"
        }), 200

@products_page.route('/products', methods=['DELETE'])
def delete_products():
    data = request.get_json()
    product_ID = data.get("product_ID")
 
    for product in products_data:
        if product("product_ID") == product_ID:
            return jsonify({
            "message": "Product deleted succesfully",
        }), 200
        
        else:
            return jsonify({
            "message": "Product does not exists"
        }), 400
            
@products_page.route('/products', methods=['PUT'])
def update_products():
    data = request.get_json()
    product_ID = data.get("product_ID")
 
    for product in products_data:
        if product("product_ID") == product_ID:
            return jsonify({
            "message": "Product updated succesfully",
        }), 200
        
        else:
            return jsonify({
            "message": "Product does not exists"
        }), 400