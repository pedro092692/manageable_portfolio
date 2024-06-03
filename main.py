from flask import Flask, url_for, redirect, render_template



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



