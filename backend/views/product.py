from flask import Flask, request, jsonify, render_template
import json
from flask_cors import CORS
import os



template_dir = os.path.abspath("/Users/eduardgol/Desktop/OurProject/WorkingDBPraktkum/frontend/templates")
app = Flask(__name__, template_folder=template_dir, static_folder=os.path.join(template_dir, 'static'))
CORS(app)

with open('/Users/eduardgol/Desktop/OurProject/WorkingDBPraktkum/backend/views/product.json', 'r') as file:
    data = json.load(file)
    
product_data = data['product_data']
 
 
@app.route('/product', methods=['GET'])
def product():
    return json.dumps({"status": "success", "data": product_data})

    
@app.route('/product', methods=['POST'])
def create_product():
    # Parse JSON data from the request
    data = request.get_json()
    # Extract product from the JSON data
    product_ID = data.get("product_ID")
 
    # Check if the products exists 
    for product in product_data:
        if product("product_ID") == product_ID:
            return jsonify({
            "message": "Product already exist",
        }), 400
        
        else:
            return jsonify({
            "message": "Product added sucsessful"
        }), 200

@app.route('/product', methods=['DELETE'])
def delete_product():
    data = request.get_json()
    product_ID = data.get("product_ID")
 
    for product in product_data:
        if product("product_ID") == product_ID:
            return jsonify({
            "message": "Product deleted succesfully",
        }), 200
        
        else:
            return jsonify({
            "message": "Product does not exists"
        }), 400
            
@app.route('/product', methods=['PUT'])
def update_product():
    data = request.get_json()
    product_ID = data.get("product_ID")
 
    for product in product_data:
        if product("product_ID") == product_ID:
            return jsonify({
            "message": "Product updated succesfully",
        }), 200
        
        else:
            return jsonify({
            "message": "Product does not exists"
        }), 400


@app.route('/product/ui', methods=['GET'])
def product_ui():
    return render_template('product.html')
   
if __name__ == '__main__':
    app.run(debug=True)