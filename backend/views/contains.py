from flask import Flask, request, jsonify, render_template
import json
import os

template_dir = os.path.abspath("C:/Users/leona/OneDrive/Desktop/DBP/WorkingDBPraktkum/frontend/templates")
app = Flask(__name__, template_folder=template_dir, static_folder=os.path.join(template_dir, 'static'))

JSON_FILE_PATH = '/Users/leona/OneDrive/Desktop/DBP/WorkingDBPraktkum/backend/views/contains.json'

def load_data():
    with open(JSON_FILE_PATH, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)

# Post Contains entry
@app.route('/contains', methods=['POST'])
def add_contains():
    data = load_data()
    new_contains = request.get_json()
    
    data['contains_data'].append(new_contains)
    save_data(data)
    return jsonify({"message": "Contains entry added successfully", "contains": new_contains}), 201

# Get Contains table & search by order_ID
@app.route('/contains', methods=['GET'])
def get_contains():
    data = load_data()
    order_id = request.args.get('order_id')
    
    if order_id:
        filtered_contains = [c for c in data['contains_data'] if c['order_ID'] == int(order_id)]
        if filtered_contains:
            return jsonify(filtered_contains)
        else:
            return jsonify({"message": "Contains entries not found"}), 404
    else:
        return jsonify(data['contains_data'])

# Patch Contains entry
@app.route('/contains/<int:order_id>/<int:product_id>', methods=['PATCH'])
def patch_contains(order_id, product_id):
    data = load_data()
    update_data = request.get_json()
    
    for contains in data['contains_data']:
        if contains['order_ID'] == order_id and contains['product_ID'] == product_id:
            for key, value in update_data.items():
                if key in contains:
                    contains[key] = value
            save_data(data)
            return jsonify({"message": "Contains entry updated successfully", "contains": contains})
    
    return jsonify({"error": "Contains entry not found"}), 404

# Delete Contains entry
@app.route('/contains/<int:order_id>/<int:product_id>', methods=['DELETE'])
def delete_contains(order_id, product_id):
    data = load_data()
    initial_length = len(data['contains_data'])
    data['contains_data'] = [c for c in data['contains_data'] if not (c['order_ID'] == order_id and c['product_ID'] == product_id)]
    
    if len(data['contains_data']) < initial_length:
        save_data(data)
        return jsonify({"message": "Contains entry deleted successfully"}), 200
    else:
        return jsonify({"error": "Contains entry not found"}), 404

# Serve the Contains UI
@app.route('/contains/ui', methods=['GET'])
def contains_ui():
    return render_template('contains.html')

if __name__ == '__main__':
    app.run(debug=True)