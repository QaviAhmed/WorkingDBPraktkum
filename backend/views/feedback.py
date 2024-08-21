from flask import Flask, request, jsonify
import json
 
with open('/Users/leona/OneDrive/Desktop/DBP/WorkingDBPraktkum/backend/views/feedback.json', 'r') as file:
    data = json.load(file)
 
feedback = data['feedback_data']

print(feedback)
 
app = Flask(__name__)
 
 
@app.route('/feedback', methods=['POST'])
def add_feedback():
    # Get the new feedback from the request body
    new_feedback = request.get_json()

    # Ensure the feedback ID is unique
    new_feedback_id = new_feedback.get('feedback_ID')
    if new_feedback_id in feed_IDs:
        return jsonify({"error": "Feedback ID already exists"}), 400

    # Add the new feedback to the data
    data['feedback_data'].append(new_feedback)

    # Update the feedback IDs list
    feed_IDs.append(new_feedback_id)

    # Save the updated data back to the JSON file
    with open('/Users/leona/OneDrive/Desktop/DBP/WorkingDBPraktkum/backend/views/feedback.json', 'w') as file:
        json.dump(data, file, indent=4)

    return jsonify({"message": "Feedback added successfully"}), 201
        
    
"""@app.route('/login', methods=['GET'])
def login_get():
    return json.dumps({"status": "success", "data": {"key": "Hello, world"}})
   """






if __name__ == '__main__':
    app.run(debug=True)