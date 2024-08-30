from flask import Flask, request, jsonify, Blueprint, render_template
from datetime import datetime
import mariadb
from db_model import db_manager
from serialization import Serialization
app = Flask(__name__)

# Assuming db_manager has already been created as shown in your initial code
order_page = Blueprint('order_page', __name__)

@order_page.route('/create_order', methods=['POST'])
def create_order():
    try:
        order_data = request.get_json()
        user_id = order_data.get('user_id')
        order_id = order_data.get('order_id')
        products = order_data.get('products', [])
        print("this are all the products: ", products, "and this the order id: ", order_id)

        if not user_id or not products:
            return jsonify({'error': 'Invalid input data'}), 400

        for product in products:
            print("this is the product: ", product )
            return  create_order_func(user_id, products, order_id)

    
    except Exception as e:
        print(f"Error in create_order: {e}")
        return jsonify({'error': 'An error occurred while processing the order'}), 500

def create_order_func(user_id, products, order_id):
    connection_obj = db_manager.connection_pool.get_connection()
    cursor = connection_obj.cursor()
    cursor.execute("START TRANSACTION;")
    
    try:
        # Begin transaction
        cursor.execute("START TRANSACTION;")
        print("this is the order id: ", order_id)

        cursor.execute("""
            INSERT INTO `Order` (order_id, status, date, price, user_id, transaction_id)
            VALUES (?, 'Pending', CURDATE(), 0, ?, NULL);
        """, (order_id,user_id,))
        # Insert into Order table
        for product in products:
            # Insert into Contains table
            cursor.execute("""
                INSERT INTO Contains (order_id, product_id, quantity)
                VALUES (?, ?, ?);
            """, (order_id, product['product_id'], product['quantity']))

            # Commit transaction
            connection_obj.commit()

        return jsonify({'message': 'Order created successfully', 'order_id': order_id}), 201

    except mariadb.Error as e:
        connection_obj.rollback()
        print(f"Error in create_order_func: {e}")
        return jsonify({'error': 'Failed to create order'}), 500

    finally:
        cursor.close()
        connection_obj.close()

oder_success_page = Blueprint('order_success_page', __name__, template_folder='/Users/qavi/Desktop/SS24/DB_Praktikum/WorkingDBPraktkum/frontend/templates/order')
@oder_success_page.route('/order-success', methods=['GET'])
def order_success():
    return render_template('orderSuccessful.html')


order_user_page = Blueprint('order_user_page', __name__,template_folder='/Users/qavi/Desktop/SS24/DB_Praktikum/WorkingDBPraktkum/frontend/templates/order')
@order_user_page.route('/user_order/<int:user_id>', methods=["GET"])
def user_order(user_id):
    user_orders = db_manager.fetch_all("""SELECT order_id, status, date, price, transaction_id FROM `Order` WHERE user_id = %s""", user_id)
    serialized_order = Serialization(user_orders, 'Order', ['order_id', 'status', 'date', 'price', 'transaction_id']).get_data()
    return render_template('myOrders.html', orders=serialized_order)

oder_track_page = Blueprint('order_track_page', __name__,template_folder='/Users/qavi/Desktop/SS24/DB_Praktikum/WorkingDBPraktkum/frontend/templates/order')
@oder_track_page.route('/track_order/<int:order_id>', methods=["GET"])
def track_order(order_id):
    
    oder_data = db_manager.fetch_all("""SELECT * FROM Contains WHERE order_id = %s""", order_id)
    serialized_order_data = Serialization(oder_data, 'Contain', ['order_id', 'product_id', 'quantity']).get_data()
    product_list = []
    for order in serialized_order_data:
        product = db_manager.fetch_all("""SELECT * FROM Product WHERE product_id = %s""", order['product_id'])
        serialized_ordered_product = Serialization(product, "Order_Product", [
        'product_id', 'product_name', 'description', 'price',
        'image', 'accessory_type', 'accessory_gender',
        'accessory_usage', 'shoe_color', 'shoe_size', 'shoe_material', 'shoe_gender'
        ]).get_data()
        product_list.append({"product": serialized_ordered_product, "quanity": order['quantity'],'order_id': order_id})
    return render_template('orderTrack.html', orders=product_list)