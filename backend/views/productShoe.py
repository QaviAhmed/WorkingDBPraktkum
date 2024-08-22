from flask import Flask, request, jsonify
import json
 
with open('backend/views/productShoe.json', 'r') as file:
    data = json.load(file)
    
productsShoe_data = data['productsShoe_data']

 
app = Flask(__name__)
 
 
@app.route('/productsShoe', methods=['GET'])
def productsShoe():
    return json.dumps({"status": "success", "data": productsShoe_data})

    
@app.route('/productsShoe', methods=['POST'])
def create_products():
    data = request.get_json()
    product_ID = data.get("product_ID")
 
    for product in productsShoe_data:
        if product("product_ID") == product_ID:
            return jsonify({
            "message": "Product already exist",
        }), 400
        
        else:
            return jsonify({
            "message": "Product added sucsessful"
        }), 200

@app.route('/productsShoe', methods=['DELETE'])
def delete_products():
    data = request.get_json()
    product_ID = data.get("product_ID")
 
    for product in productsShoe_data:
        if product("product_ID") == product_ID:
            return jsonify({
            "message": "Product deleted succesfully",
        }), 200
        
        else:
            return jsonify({
            "message": "Product does not exists"
        }), 400
            
@app.route('/productsShoe', methods=['PUT'])
def update_products():
    data = request.get_json()
    product_ID = data.get("product_ID")
 
    for product in productsShoe_data:
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