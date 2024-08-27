from flask import Flask, request, jsonify, render_template, Blueprint, redirect, url_for, flash
from jinja2 import TemplateNotFound
import json
from db_model import db_manager
from serialization import Serialization
import os
from collections import namedtuple
 
template_dir = os.path.abspath("/Users/qavi/Desktop/SS24/DB_Praktikum/WorkingDBPraktkum/frontend/templates")

products_page = Blueprint('product_page', __name__,
                        template_folder=f"{template_dir}/main")

# -- all products calls --
@products_page.route('/', methods=['GET'])
def products():
    category_id = request.args.get('category_id')
    search_query = request.args.get('search')
    
    # Base query with joins
    query = """
    SELECT 
        p.product_id,
        p.name AS product_name,
        p.description,
        p.price,
        p.image,
        p.accessory_type,
        p.accessory_gender,
        p.accessory_usage,
        p.shoe_color,
        p.shoe_size,
        p.shoe_material,
        p.shoe_gender,
        c.category_id,
        c.name AS category_name
    FROM 
        Product p
    JOIN 
        BelongsTo b ON p.product_id = b.product_id
    JOIN 
        Category c ON b.category_id = c.category_id
    """
    
    # Filtering by category if category_id is provided
    if category_id:
        query += f" WHERE c.category_id = {category_id}"
    
    # Searching if search_query is provided
    if search_query:
        if 'WHERE' in query:
            query += f" AND p.name LIKE '%{search_query}%'"
        else:
            query += f" WHERE p.name LIKE '%{search_query}%'"
    
    # Fetch data from database
    products_data = db_manager.fetch_all(query)
    serialized_data = Serialization(products_data, "Product", [
        'product_id', 'product_name', 'description', 'price',
        'image', 'accessory_type', 'accessory_gender',
        'accessory_usage', 'shoe_color', 'shoe_size', 'shoe_material', 'shoe_gender',
        'category_id', 'category_name'
    ]).get_data()
    
    return render_template('index.html', products_data=serialized_data)

@products_page.route('/products/combined', methods=['GET'])
def combined_products():
    query = """
    SELECT p.product_id, p.name, p.price
    FROM Product p
    WHERE p.price < 50
    
    UNION
    
    SELECT p.product_id, p.name, p.price
    FROM Product p
    WHERE p.price BETWEEN 50 AND 100
    """
    
    products_data = db_manager.fetch_all(query)
    serialized_data = Serialization(products_data, "Product", ['product_id', 'name', 'price']).get_data()
    
    return render_template('index.html', products_data=serialized_data)

@products_page.route('/products/intersect', methods=['GET'])
def intersect_products():
    query = """
    SELECT p.product_id, p.name
    FROM Product p
    WHERE p.price > 30
    
    INTERSECT
    
    SELECT p.product_id, p.name
    FROM Product p
    WHERE p.price < 100
    """
    
    products_data = db_manager.fetch_all(query)
    serialized_data = Serialization(products_data, "Product", [
    'product_id', 'product_name', 'description', 'price',
    'image', 'accessory_type', 'accessory_gender',
    'accessory_usage', 'shoe_color', 'shoe_size', 'shoe_material', 'shoe_gender',
    'category_id', 'category_name'
    ]).get_data()
    
    return render_template('index.html', products_data=serialized_data)

@products_page.route('/products/difference', methods=['GET'])
def difference_products():
    query = """
    SELECT p.product_id, p.name
    FROM Product p
    WHERE p.price < 50
    
    EXCEPT
    
    SELECT p.product_id, p.name
    FROM Product p
    WHERE p.price < 20
    """
    
    products_data = db_manager.fetch_all(query)
    serialized_data = Serialization(products_data, "Product", [
    'product_id', 'product_name', 'description', 'price',
    'image', 'accessory_type', 'accessory_gender',
    'accessory_usage', 'shoe_color', 'shoe_size', 'shoe_material', 'shoe_gender',
    'category_id', 'category_name'
    ]).get_data()
    
    return render_template('index.html', products_data=serialized_data)

 # -- product cruds --
@products_page.route('/products', methods=['POST'])
def create_product():
    product_id = request.form.get('product_id')
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    
    # Check if the product exists
    existing_product = db_manager.fetch_one("SELECT * FROM Product WHERE product_id = %s", (product_id,))
    if existing_product:
        flash("Product already exists", "error")
        return redirect(url_for('main_page'))
    
    # Insert new product
    try:
        db_manager.execute("""
        INSERT INTO Product (product_id, name, description, price)
        VALUES (%s, %s, %s, %s)
        """, (product_id, name, description, price))
        flash("Product added successfully", "success")
    except Exception as e:
        flash(f"Error adding product: {str(e)}", "error")
    
    return redirect(url_for('main_page'))

@products_page.route('/products', methods=['DELETE'])
def delete_product():
    product_id = request.form.get('product_id')
    
    # Check if the product exists
    existing_product = db_manager.fetch_one("SELECT * FROM Product WHERE product_id = %s", (product_id,))
    if not existing_product:
        flash("Product does not exist", "error")
        return redirect(url_for('main_page'))
    
    # Delete the product
    try:
        db_manager.execute("DELETE FROM Product WHERE product_id = %s", (product_id,))
        flash("Product deleted successfully", "success")
    except Exception as e:
        flash(f"Error deleting product: {str(e)}", "error")
    
    return redirect(url_for('main_page'))

@products_page.route('/products', methods=['PUT'])
def update_product():
    product_id = request.form.get('product_id')
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    
    # Check if the product exists
    existing_product = db_manager.fetch_one("SELECT * FROM Product WHERE product_id = %s", (product_id,))
    if not existing_product:
        flash("Product does not exist", "error")
        return redirect(url_for('main_page'))
    
    # Update the product
    try:
        db_manager.execute("""
        UPDATE Product
        SET name = %s, description = %s, price = %s
        WHERE product_id = %s
        """, (name, description, price, product_id))
        flash("Product updated successfully", "success")
    except Exception as e:
        flash(f"Error updating product: {str(e)}", "error")
    
    return redirect(url_for('main_page'))

# -- detail page for products --

product_detail_page = Blueprint('product_detail_page', __name__,
                        template_folder=f"{template_dir}/product_detail")


@product_detail_page.route('/product/<int:product_id>', methods=['GET'])
def product_detail(product_id):
    print("this is to check the product id: ", product_id)
    product = db_manager.fetch_one("SELECT * FROM Product WHERE product_id = %s", (product_id))
    Product = namedtuple('Product', [
        'product_id', 'product_name', 'description', 'price',
        'image', 'accessory_type', 'accessory_gender',
        'accessory_usage', 'shoe_color', 'shoe_size', 'shoe_material', 'shoe_gender',
        'category_id', 'category_name'
    ])
    product_dict = Product(*product)._asdict()
    print("this for checking the product: ", product_dict)
    if not product:
        flash("Product not found", "error")
        return redirect(url_for('main_page'))
    
    # Assuming you have a template for the product detail page
    return render_template('product_detail.html', product=product_dict)
