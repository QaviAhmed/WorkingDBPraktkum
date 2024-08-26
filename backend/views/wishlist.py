from flask import Flask, request, jsonify, render_template
import json
import os

template_dir = os.path.abspath("/Users/Roman/Downloads/WorkingDBPraktkum/frontend/templates")
app = Flask(__name__, template_folder=template_dir, static_folder=os.path.join(template_dir, 'static'))

with open('backend/views/wishlist.json', 'r') as file:
    data = json.load(file)
    
wishlist_data = data['wishlist_data']
 
@app.route('/wishlist', methods=['GET'])
def product_accessories():
    return json.dumps({"status": "success", "data": wishlist_data})

    
@app.route('/wishlist', methods=['POST'])
def create_wishlist():
    data = request.get_json()
    product_ID = data.get("product_ID")
 
    for product in wishlist_data:
        if product("product_ID") == product_ID:
            return jsonify({
            "message": "Product already exist",
        }), 400
        
        else:
            return jsonify({
            "message": "Product added sucsessful"
        }), 200

@app.route('/wishlist', methods=['DELETE'])
def delete_wishlist():
    data = request.get_json()
    product_ID = data.get("product_ID")
 
    for product in wishlist_data:
        if product("product_ID") == product_ID:
            return jsonify({
            "message": "Product deleted succesfully",
        }), 200
        
        else:
            return jsonify({
            "message": "Product does not in wishlist"
        }), 400
            
@app.route('/wishlist', methods=['PUT'])
def update_wishlist():
    data = request.get_json()
    product_ID = data.get("product_ID")
 
    for product in wishlist_data:
        if product("product_ID") == product_ID:
            return jsonify({
            "message": "Product updated succesfully",
        }), 200
        
        else:
            return jsonify({
            "message": "Product does not exists"
        }), 400

@app.route('/wishlist/ui', methods=['GET'])
def product_ui():
    return render_template('wishlist.html')

if __name__ == '__main__':
    app.run(debug=True)