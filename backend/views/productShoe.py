from flask import Flask, request, jsonify, render_template
import json
import os

template_dir = os.path.abspath("/Users/Roman/Downloads/WorkingDBPraktkum/frontend/templates")
app = Flask(__name__, template_folder=template_dir, static_folder=os.path.join(template_dir, 'static'))

with open('backend/views/productShoe.json', 'r') as file:
    data = json.load(file)
    
productShoe_data = data['productShoe_data']
 
@app.route('/productShoe', methods=['GET'])
def productsShoe():
    return json.dumps({"status": "success", "data": productShoe_data})

    
@app.route('/productShoe', methods=['POST'])
def create_products():
    data = request.get_json()
    product_ID = data.get("product_ID")
 
    for product in productShoe_data:
        if product("product_ID") == product_ID:
            return jsonify({
            "message": "Product already exist",
        }), 400
        
        else:
            return jsonify({
            "message": "Product added sucsessful"
        }), 200

@app.route('/productShoe', methods=['DELETE'])
def delete_products():
    data = request.get_json()
    product_ID = data.get("product_ID")
 
    for product in productShoe_data:
        if product("product_ID") == product_ID:
            return jsonify({
            "message": "Product deleted succesfully",
        }), 200
        
        else:
            return jsonify({
            "message": "Product does not exists"
        }), 400
            
@app.route('/productShoe', methods=['PUT'])
def update_products():
    data = request.get_json()
    product_ID = data.get("product_ID")
 
    for product in productShoe_data:
        if product("product_ID") == product_ID:
            return jsonify({
            "message": "Product updated succesfully",
        }), 200
        
        else:
            return jsonify({
            "message": "Product does not exists"
        }), 400

@app.route('/productShoe/ui', methods=['GET'])
def product_ui():
    return render_template('productShoe.html')
   
if __name__ == '__main__':
    app.run(debug=True)