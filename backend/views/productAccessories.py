from flask import Flask, request, jsonify, render_template
import json
import os

template_dir = os.path.abspath("/Users/Roman/Downloads/WorkingDBPraktkum/frontend/templates")
app = Flask(__name__, template_folder=template_dir, static_folder=os.path.join(template_dir, 'static'))

with open('/Users/Roman/Downloads/WorkingDBPraktkum/backend/views/productAccessories.json', 'r') as file:
    data = json.load(file)
    
product_accessories_data = data['product_accessories_data']
 
@app.route('/productAccessories', methods=['GET'])
def product_accessories():
    return json.dumps({"status": "success", "data": product_accessories_data})

    
@app.route('/productAccessories', methods=['POST'])
def create_products_accessories():
    data = request.get_json()
    product_ID = data.get("product_ID")
 
    for product in product_accessories_data:
        if product("product_ID") == product_ID:
            return jsonify({
            "message": "Product already exist",
        }), 400
        
        else:
            return jsonify({
            "message": "Product added sucsessful"
        }), 200

@app.route('/productAccessories', methods=['DELETE'])
def delete_products_accessories():
    data = request.get_json()
    product_ID = data.get("product_ID")
 
    for product in product_accessories_data:
        if product("product_ID") == product_ID:
            return jsonify({
            "message": "Product deleted succesfully",
        }), 200
        
        else:
            return jsonify({
            "message": "Product does not exists"
        }), 400
            
@app.route('/productAccessories', methods=['PUT'])
def update_products_accessories():
    data = request.get_json()
    product_ID = data.get("product_ID")
 
    for product in product_accessories_data:
        if product("product_ID") == product_ID:
            return jsonify({
            "message": "Product updated succesfully",
        }), 200
        
        else:
            return jsonify({
            "message": "Product does not exists"
        }), 400
            
@app.route('/productAccessories/ui', methods=['GET'])
def product_ui():
    return render_template('productAccessories.html')

   
if __name__ == '__main__':
    app.run(debug=True)