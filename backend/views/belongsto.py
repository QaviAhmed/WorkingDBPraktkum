from flask import Flask, request, jsonify, render_template
import json
import os

template_dir = os.path.abspath("C:/Users/leona/OneDrive/Desktop/DBP/WorkingDBPraktkum/frontend/templates")
app = Flask(__name__, template_folder=template_dir, static_folder=os.path.join(template_dir, 'static'))

JSON_FILE_PATH = '/Users/leona/OneDrive/Desktop/DBP/WorkingDBPraktkum/backend/views/belongsto.json'

def load_data():
    with open(JSON_FILE_PATH, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)

# Post BelongsTo entry
@app.route('/belongsto', methods=['POST'])
def add_belongsto():
    data = load_data()
    new_belongsto = request.get_json()
    
    data['belongsto_data'].append(new_belongsto)
    save_data(data)
    return jsonify({"message": "BelongsTo entry added successfully", "belongsto": new_belongsto}), 201

# Get BelongsTo table & search by order_ID
@app.route('/belongsto', methods=['GET'])
def get_belongsto():
    data = load_data()
    category_id = request.args.get('category_id')
    
    if category_id:
        filtered_belongsto = [b for b in data['belongsto_data'] if b['category_ID'] == int(category_id)]
        if filtered_belongsto:
            return jsonify(filtered_belongsto)
        else:
            return jsonify({"message": "BelongsTo entries not found"}), 404
    else:
        return jsonify(data['belongsto_data'])

# Patch BelongsTo entry
@app.route('/belongsto/<int:category_id>/<int:product_id>', methods=['PATCH'])
def patch_belongsto(category_id, product_id):
    data = load_data()
    update_data = request.get_json()
    
    for belongsto in data['belongsto_data']:
        if belongsto['category_ID'] == category_id and belongsto['product_ID'] == product_id:
            for key, value in update_data.items():
                if key in belongsto:
                    belongsto[key] = value
            save_data(data)
            return jsonify({"message": "BelongsTo entry updated successfully", "belongsto": belongsto})
    
    return jsonify({"error": "BelongsTo entry not found"}), 404

# Delete BelongsTo entry
@app.route('/belongsto/<int:category_id>/<int:product_id>', methods=['DELETE'])
def delete_belongsto(category_id, product_id):
    data = load_data()
    initial_length = len(data['belongsto_data'])
    data['belongsto_data'] = [b for b in data['belongsto_data'] if not (b['category_ID'] == category_id and b['product_ID'] == product_id)]
    
    if len(data['belongsto_data']) < initial_length:
        save_data(data)
        return jsonify({"message": "BelongsTo entry deleted successfully"}), 200
    else:
        return jsonify({"error": "BelongsTo entry not found"}), 404

# Serve the BelongsTo UI
@app.route('/belongsto/ui', methods=['GET'])
def belongsto_ui():
    return render_template('belongsto.html')

if __name__ == '__main__':
    app.run(debug=True)
