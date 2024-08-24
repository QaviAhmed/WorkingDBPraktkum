from flask import Flask, request, jsonify, render_template, send_from_directory
import json
import os
from flask_cors import CORS

template_dir = os.path.abspath("/Users/eduardgol/Desktop/OurProject/WorkingDBPraktkum/frontend/templates")
app = Flask(__name__, template_folder=template_dir, static_folder=os.path.join(template_dir, 'static'))
CORS(app)

JSON_FILE_PATH = '/Users/eduardgol/Desktop/OurProject/WorkingDBPraktkum/backend/views/feedback.json'

def load_data():
    with open(JSON_FILE_PATH, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)

# Post feedback entity ++ feedback_ID is 'generated'
@app.route('/feedback/ui', methods=['GET'])
def feedback_ui():
    return render_template('feedback.html')

@app.route('/feedback', methods=['POST'])
def add_feedback():
    data = load_data()
    new_feedback = request.get_json()
    
    # Generate feedback_ID
    max_id = max([f['feedback_ID'] for f in data['feedback_data']], default=0)
    new_feedback['feedback_ID'] = max_id + 1
    
    data['feedback_data'].append(new_feedback)
    save_data(data)
    return jsonify({"message": "Feedback added successfully", "feedback": new_feedback}), 201

# Get feedback table & search feedbacks by product_id
@app.route('/feedback', methods=['GET'])
def get_feedback():
    data = load_data()
    product_id = request.args.get('product_id')
    
    if product_id:
        filtered_feedback = [f for f in data['feedback_data'] if f['product_ID'] == int(product_id)]
        if len(filtered_feedback) != 0:
            return jsonify(filtered_feedback)
        else:
            return jsonify({"message": "Feedback not"}), 404
    else:
        return jsonify(data['feedback_data'])


# Patch
@app.route('/feedback/<int:feedback_id>', methods=['PATCH'])
def patch_feedback(feedback_id):
    data = load_data()
    update_data = request.get_json()
    
    for feedback in data['feedback_data']:
        if feedback['feedback_ID'] == feedback_id:
            for key, value in update_data.items():
                if key in feedback:
                    feedback[key] = value
            save_data(data)
            return jsonify({"message": "Feedback updated successfully", "feedback": feedback})
    
    return jsonify({"error": "Feedback not found"}), 404

# Delete
''' @app.route('/feedback/<int:feedback_id>', methods=['DELETE'])
def delete_feedback(feedback_id):
    data = load_data()
    initial_length = len(data['feedback_data'])
    data['feedback_data'] = [f for f in data['feedback_data'] if f['feedback_ID'] != feedback_id]
    
    if len(data['feedback_data']) < initial_length:
        save_data(data)
        return jsonify({"message": "Feedback deleted successfully"}), 200
    else:
        return jsonify({"error": "Feedback not found"}), 404

# Serve the feedback UI'''


if __name__ == '__main__':
    app.run(debug=True)
