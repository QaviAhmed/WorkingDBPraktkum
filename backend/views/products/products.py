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
    
    if category_id:
        # Call the stored procedure for category filtering
        query = "CALL GetProductsByCategory(%s)"
        params = (category_id,)
    elif search_query:
        # Call the stored procedure for search functionality
        query = "CALL SearchProductsByName(%s)"
        params = (search_query,)
    else:
        # Default to fetching all products without filtering or searching
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
        GROUP BY 
            c.category_id, p.product_id
        HAVING 
            p.price > 0
        ORDER BY 
            p.price ASC;
        """
        params = ()
    
    # Fetch data from the database
    products_data = db_manager.fetch_all(query, params)
    
    # Serialize the fetched data
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
    # uncorelated
    query = """
        SELECT p.product_id, p.name
        FROM Product p
        WHERE p.price > 30
        AND p.product_id IN (
            SELECT product_id
            FROM BelongsTo
            WHERE category_id IN (
                SELECT category_id
                FROM BelongsTo
                GROUP BY category_id
                HAVING COUNT(product_id) > 5
            )
        )
        
        INTERSECT
        
        SELECT p.product_id, p.name
        FROM Product p
        WHERE p.price < 100
        AND p.product_id IN (
            SELECT product_id
            FROM BelongsTo
            WHERE category_id IN (
                SELECT category_id
                FROM BelongsTo
                GROUP BY category_id
                HAVING COUNT(product_id) > 5
            )
        )
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
    # correlated
    query = """
            SELECT p.product_id, p.name
            FROM Product p
            WHERE p.price < 50
            AND EXISTS (
                SELECT 1
                FROM Category c
                WHERE c.category_id = p.product_id
                AND c.name = 'Shoes'
            )
            
            EXCEPT
            
            SELECT p.product_id, p.name
            FROM Product p
            WHERE p.price < 20
            AND NOT EXISTS (
                SELECT 1
                FROM Feedback f
                WHERE f.product_ID = p.product_id
                AND f.rating < 3
            )
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
    print(product)
    Product = namedtuple('Product', [
        'product_id', 'product_name', 'description', 'price',
        'image', 'accessory_type', 'accessory_gender',
        'accessory_usage', 'shoe_color', 'shoe_size', 'shoe_material', 'shoe_gender'
    ])
    product_dict = Product(*product)._asdict()
    print("this for checking the product: ", product_dict)
    if not product:
        flash("Product not found", "error")
        return redirect(url_for('main_page'))
    
        # Fetch feedback related to the product
    feedback = db_manager.fetch_all(
        "SELECT * FROM Feedback WHERE product_ID = %s", (product_id,)
    )
    print(feedback)
    # Assuming you have a template for the product detail page
    return render_template('product_detail.html', product=product_dict, feedback=feedback)

# -- category page functions --

category_page = Blueprint('category_page', __name__)

@category_page.app_context_processor
def inject_categories():
    categories = db_manager.fetch_all("SELECT * FROM Category")
    print("this is for the categories: ", categories)
    serialized_data = Serialization(categories, 'Categories', [
        'category_id', 'category_name'
    ]).get_data()
    

    return {'categories': serialized_data}

# -- feedback functions --
feedback_page = Blueprint('feedback_page', __name__)
@feedback_page.route('/feedback', methods=['POST', 'GET'])
def handle_feedback():
    if request.method == 'POST':
        # Handle POST request logic
        feedback_data = request.get_json()
        
        # Validate that all required fields are present
        if not all(key in feedback_data for key in ['user_ID', 'product_ID', 'rating', 'comment']):
            return jsonify({"error": "Missing data"}), 400

        # Generate feedback_ID (assuming it's AUTO_INCREMENT in the DB)
        feedback_id = db_manager.fetch_one("SELECT COALESCE(MAX(feedback_ID), 0) FROM Feedback")[0] + 1
        
        # Insert the feedback into the database
        db_manager.execute_query(
            """INSERT INTO Feedback (feedback_ID, user_ID, product_ID, rating, comment) 
            VALUES (%s, %s, %s, %s, %s)""",
            feedback_id, feedback_data['user_ID'], feedback_data['product_ID'],
            feedback_data['rating'], feedback_data['comment']
        )
        
        return jsonify({"message": "Feedback added successfully", "feedback_id": feedback_id}), 201

    elif request.method == 'GET':
        product_id = request.args.get('product_id')
        
        if product_id:
            try:
                product_id = int(product_id)  # Ensure product_id is an integer
                print(product_id)
                feedbacks = db_manager.fetch_all(f"""SELECT * FROM Feedback WHERE product_ID = {product_id}""")
                
                if feedbacks:
                    return jsonify(feedbacks)
                else:
                    return jsonify({"message": "No feedback found for this product"}), 404
            except ValueError:
                return jsonify({"message": "Invalid product ID"}), 400
        else:
            return jsonify({"message": "Product ID not provided"}), 400

