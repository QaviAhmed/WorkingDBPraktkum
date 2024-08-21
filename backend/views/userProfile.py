from flask import Flask, request, jsonify, render_template
import json
import os

template_dir = os.path.abspath("/Users/eduardgol/Desktop/OurProject/WorkingDBPraktkum/frontend/templates")

with open('/Users/eduardgol/Desktop/OurProject/WorkingDBPraktkum/backend/views/users.json', 'r') as file:
    data = json.load(file)

users = data['users_data']

app = Flask(__name__, template_folder=template_dir)
 
 
@app.route('/userProfile/<int:user_id>', methods=['GET', 'POST'])
def getUserProfile(user_id):
    if request.method == 'GET':
        for user in users:
            if user["user_ID"] == user_id:
                 return render_template('userProfile.html', user=user)
        
    else:
        return render_template('home.html')

        
'''@app.route("/userProfile/<user_id>", methods=['GET', 'PUT'])
def update_destroy_accounts(account_id):
    if request.method == 'GET': return retrieve_account_controller(account_id)
    if request.method == 'PUT': return update_account_controller(account_id)
    else: return 'Method is Not Allowed'   '''

if __name__ == '__main__':
    app.run(debug=True)
