from flask import Flask, url_for, redirect, render_template
from flask_login import login_user, LoginManager, current_user, logout_user, login_required


# INIT APP
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return 'admin panel'


if __name__ == '__main__':
    app.run(debug=True)



