from flask import Flask, url_for, redirect, render_template, request, flash
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from database import Database
from send_email import Email
from forms import LoginForm, RecentWork, PhotoProfile
from flask_bootstrap import Bootstrap5


# INIT APP
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
csfr = CSRFProtect(app)

# DATABASE
db = Database(app)
# Create tables
db.create_tables()

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
    all_works = db.get_all_works()
    return render_template('admin-work.html', all_works=all_works)


@app.route('/admin/personal', methods=['GET', 'POST'])
def personal():
    form_photo_profile = PhotoProfile()
    if form_photo_profile.validate_on_submit():
        print('hello photo')
    return render_template('admin-personal.html', form_photo_profile=form_photo_profile)


@app.route('/admin/page', methods=['GET'])
def page():
    return render_template('page-info.html')


@app.route('/admin/add-work', methods=['GET', 'POST'])
def add_work():
    form = RecentWork()
    if form.validate_on_submit():
        title = form.title.data
        text_info = form.text_info.data
        image_url = form.img_url.data
        work_url = form.work_url.data

        db.create_work(title, text_info, image_url, work_url)

        return redirect(url_for('admin'))

    return render_template('add-work.html', form=form)


@app.route('/admin/work/edit/<work_id>', methods=['GET', 'POST'])
def work_edit(work_id):
    work = db.get_work(work_id)
    form_edit = RecentWork(
        title=work.title,
        text_info=work.text_info,
        img_url=work.image_url,
        work_url=work.work_url
    )
    if form_edit.submit.data and form_edit.validate():

        title = form_edit.title.data
        work_text = form_edit.text_info.data
        img_url = form_edit.img_url.data
        work_url = form_edit.work_url.data

        db.edit_work(work, title, work_text, img_url, work_url)

        return redirect(url_for('admin'))

    if request.method == 'POST' and 'work_id' in request.form:
        db.delete_work(work)

        return redirect(url_for('admin'))

    return render_template('add-work.html', form=form_edit, work_id=work.id)


if __name__ == '__main__':
    app.run(debug=True)



