from flask import Flask, render_template, Blueprint
import os
from views.login import login_page
from views.registration import register_page
from views.userProfile import user_page

    
template_dir = os.path.abspath("/Users/eduardgol/Desktop/OurProject/WorkingDBPraktkum/frontend/templates")
app = Flask(__name__, template_folder=template_dir)
app.register_blueprint(login_page)
app.register_blueprint(register_page)
app.register_blueprint(user_page)


@app.route("/", methods=['GET'])
def index():
    return render_template('main.html')


if __name__ == "__main__":
    app.run(debug=True)




