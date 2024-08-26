from flask import Flask, request, jsonify, render_template
import json
import os

template_dir = os.path.abspath("/Users/Roman/Downloads/WorkingDBPraktkum/frontend/templates")
app = Flask(__name__, template_folder=template_dir, static_folder=os.path.join(template_dir, 'static'))

PRODUCT_JSON_FILE_PATH = '/Users/Roman/Downloads/WorkingDBPraktkum/backend/views/product.json'

def load_data():
    with open(PRODUCT_JSON_FILE_PATH, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(PRODUCT_JSON_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)

# Get products
@app.route('/product', methods=['GET'])
def get_products():
    data = load_data()
    search_product_id = request.args.get('search_product_ID')

    if search_product_id:
        try:
            search_product_id = int(search_product_id)
            filtered_products = [p for p in data['product_data'] if p['product_ID'] == search_product_id]

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(filtered_products)
            else:
                return render_template("product.html", products=filtered_products, search_id=search_product_id)
        except ValueError:
            error_message = f"Invalid product ID: {search_product_id}"
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"error": error_message}), 400
            else:
                return render_template("product.html", error=error_message)
    else:
        return render_template("product.html", products=data['product_data'])

# Add new product
@app.route('/product', methods=['POST'])
def add_product():
    data = load_data()
    new_product = request.get_json()

    # Generate product_ID
    max_id = max([product['product_ID'] for product in data['product_data']], default=0)
    new_product['product_ID'] = max_id + 1

    # Ensure all required fields are present
    required_fields = ['name', 'description', 'price', 'image']
    for field in required_fields:
        if field not in new_product:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    data['product_data'].append(new_product)
    save_data(data)
    return jsonify({"message": "Product added successfully", "product": new_product}), 201

# Update product
@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = load_data()
    update_data = request.get_json()

    for product in data['product_data']:
        if product['product_ID'] == product_id:
            product.update(update_data)
            save_data(data)
            return jsonify({"message": "Product updated successfully", "product": product})

    return jsonify({"error": "Product not found"}), 404

# Delete product
@app.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    data = load_data()

    for index, product in enumerate(data['product_data']):
        if product['product_ID'] == product_id:
            del data['product_data'][index]
            save_data(data)
            return jsonify({"message": "Product deleted successfully"}), 200

    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
