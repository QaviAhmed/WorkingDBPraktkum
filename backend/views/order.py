from flask import Flask, request, jsonify, render_template
import json
import os

template_dir = os.path.abspath("C:/Users/leona/OneDrive/Desktop/DBP/WorkingDBPraktkum/frontend/templates")
app = Flask(__name__, template_folder=template_dir, static_folder=os.path.join(template_dir, 'static'))

JSON_FILE_PATH = '/Users/leona/OneDrive/Desktop/DBP/WorkingDBPraktkum/backend/views/order.json'  # Update this path

def load_data():
    with open(JSON_FILE_PATH, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)

# Get all orders or search by user_ID
@app.route('/order', methods=['GET'])
def get_orders():
    data = load_data()
    user_id = request.args.get('user_id')
    
    if user_id:
        filtered_orders = [order for order in data['order_data'] if order['user_ID'] == int(user_id)]
        return jsonify(filtered_orders)
    else:
        return jsonify(data['order_data'])

# Add new order
@app.route('/order', methods=['POST'])
def add_order():
    data = load_data()
    new_order = request.get_json()
    
    # Generate order_ID
    max_id = max([order['order_ID'] for order in data['order_data']], default=0)
    new_order['order_ID'] = max_id + 1
    
    data['order_data'].append(new_order)
    save_data(data)
    return jsonify({"message": "Order added successfully", "order": new_order}), 201

# Update order
@app.route('/order/<int:order_id>', methods=['PATCH'])
def update_order(order_id):
    data = load_data()
    update_data = request.get_json()
    
    for order in data['order_data']:
        if order['order_ID'] == order_id:
            order.update(update_data)
            save_data(data)
            return jsonify({"message": "Order updated successfully", "order": order})
    
    return jsonify({"error": "Order not found"}), 404

# Delete order
@app.route('/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    data = load_data()
    initial_length = len(data['order_data'])
    data['order_data'] = [order for order in data['order_data'] if order['order_ID'] != order_id]
    
    if len(data['order_data']) < initial_length:
        save_data(data)
        return jsonify({"message": "Order deleted successfully"}), 200
    else:
        return jsonify({"error": "Order not found"}), 404

# Serve the order UI
@app.route('/order/ui', methods=['GET'])
def order_ui():
    return render_template('order.html')

if __name__ == '__main__':
    app.run(debug=True)