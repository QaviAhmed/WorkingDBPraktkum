from flask import Flask, request, jsonify
import json
 
 
# data = users
#   return json.dumps({"status": "success", "data": data})
 
with open('/Users/Roman/Downloads/DB_Praktikum/WorkingDBPraktkum/backend/views/products.json', 'r') as file:
    data = json.load(file)
    
products_data = data['products_data']

 
app = Flask(__name__)
 
 
@app.route('/products', methods=['GET'])
def products():
    return json.dumps({"status": "success", "data": products_data})

    
@app.route('/products', methods=['POST'])
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

@app.route('/products', methods=['DELETE'])
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
            
@app.route('/products', methods=['PUT'])
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

   
if __name__ == '__main__':
    app.run(debug=True)