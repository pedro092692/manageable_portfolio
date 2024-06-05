from flask import Flask, url_for, redirect, render_template, request, flash
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from send_email import Email
from forms import LoginForm
from flask_bootstrap import Bootstrap5


# INIT APP
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

# PLUGINS
Bootstrap5(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = Email()
        name = request.form.get('name')
        email_sender = request.form.get('email')
        message = request.form.get('message')
        # send_email = email.send_email(message, email_sender=email_sender, name=name)
        send_email = True
        if send_email:
            flash('Message sent I will contact you as soon as possible.')

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')


@app.route('/admin/add-work', methods=['GET'])
def add_work():
    return 'add some work...'


if __name__ == '__main__':
    app.run(debug=True)



