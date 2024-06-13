from flask import Flask, url_for, redirect, render_template, request, flash
from flask_wtf.csrf import CSRFProtect
from database import Database
from send_email import Email
from forms import *
from flask_bootstrap import Bootstrap5
from helpers import get_avatar_extension, get_info_page, save_img_file
from flask_security import login_required
from flask_mailman import Mail
from dotenv import load_dotenv
import os

# load env
load_dotenv()

# INIT APP
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_POST_LOGIN_VIEW'] = '/admin'
# Mail Config
app.config['MAIL_SERVER'] = os.environ.get('SERVER')
app.config['MAIL_PORT'] = os.environ.get('PORT')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('USER')
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('USER')
mail = Mail(app)
csfr = CSRFProtect(app)

# DATABASE
db = Database(app)
# Create tables
db.create_tables()

# PLUGINS
Bootstrap5(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    # media
    # get file extension
    file = get_avatar_extension(file_name='avatar')
    file_extension = ''

    if file:
        file_extension = file.split('.')[1]

    if file_extension:
        photo_name = f'avatar.{file_extension}'
    else:
        photo_name = ''

    email = get_info_page(db=db, type_info='email')
    bio = get_info_page(db=db, type_info='bio')
    social_networks = db.all_social()
    works = db.get_all_works()
    main_title = get_info_page(db=db, type_info='page_title')
    main_text = get_info_page(db=db, type_info='main_text')
    get_in_touch_title = get_info_page(db=db, type_info='get_in_touch_title')
    get_in_touch_text = get_info_page(db=db, type_info='get_in_touch_text')

    media = {
        'photo_profile': photo_name
    }

    page_data = {
        'email': email,
        'bio': bio,
        'social_networks': social_networks,
        'works': works,
        'main_title': main_title,
        'main_text': main_text,
        'get_in_touch_title': get_in_touch_title,
        'get_in_touch_text': get_in_touch_text,
        'name': db.get_user(user_id=1).name
    }

    if request.method == 'POST':
        email = Email()
        name = request.form.get('name')
        email_sender = request.form.get('email')
        message = request.form.get('message')
        send_email = email.send_email(message, email_sender=email_sender, name=name)
        send_email = True
        if send_email:
            flash('Message sent I will contact you as soon as possible.')

    return render_template('index.html', media=media, page_data=page_data)


@app.route('/admin', methods=['GET'])
@login_required
def admin():
    all_works = db.get_all_works()
    return render_template('admin-work.html', all_works=all_works)


@app.route('/admin/personal', methods=['GET', 'POST'])
@login_required
def personal():
    # photo profile
    form_photo_profile = PhotoProfile()
    if form_photo_profile.submit_photo.data and form_photo_profile.validate():
        # save img
        save_img_file(img_type='avatar', img=form_photo_profile.photo.data)
        flash('Photo profile updated')

    # Email info
    email_info = get_info_page(db=db, type_info='email')

    email_form = Email(email=email_info)

    if email_form.submit_email.data and email_form.validate():
        email = email_form.email.data
        db.add_page_info(info_type='email', value=email)

        flash('Email updated')

    # Given name info
    user = db.get_user(user_id=1)

    name_form = GivenName(
        name=user.name
    )
    if name_form.submit_name.data and name_form.validate():
        db.add_name(name=name_form.name.data)
        flash('Given name updated.')

    # Bio info
    bio_info = get_info_page(db=db, type_info='bio')
    bio_form = Bio(bio=bio_info)

    if bio_form.submit_bio.data and bio_form.validate():
        bio_info = bio_form.bio.data
        db.add_page_info(info_type='bio', value=bio_info)

        flash('Bio info updated')

    # Social Networks
    all_networks = db.all_social()

    return render_template('admin-personal.html', form_photo_profile=form_photo_profile, email_form=email_form,
                           bio_form=bio_form, name_form=name_form, social_networks=all_networks)


@app.route('/admin/page', methods=['GET', 'POST'])
@login_required
def page():
    # Main title text
    main_title_info = get_info_page(db=db, type_info='page_title')
    main_title_form = PageMainTitle(
        title=main_title_info
    )
    if main_title_form.submit_title.data and main_title_form.validate():
        title = main_title_form.title.data
        db.add_page_info(info_type='page_title', value=title)
        flash('Main title Updated.')

    # header bg
    header_img_form = PhotoProfile()
    if header_img_form.submit_photo.data and header_img_form.validate():
        # save image file
        img = header_img_form.photo.data
        save_img_file(img_type='bg', img=img)

        flash('header Background updated')

    # Main text
    main_text_info = get_info_page(db=db, type_info='main_text')
    main_text_form = MainText(
        text=main_text_info
    )

    if main_text_form.submit_text.data and main_title_form.validate():
        text = main_text_form.text.data
        db.add_page_info(info_type='main_text', value=text)

        flash('Main Text Updated.')

    # Get in touch title
    get_in_touch_title_info = get_info_page(db=db, type_info='get_in_touch_title')
    get_in_touch_title_form = GetInTouch(
        title=get_in_touch_title_info
    )

    if get_in_touch_title_form.submit_get_in_touch_title.data and get_in_touch_title_form.validate():
        title = get_in_touch_title_form.title.data
        db.add_page_info(info_type='get_in_touch_title', value=title)

        flash('Get In Touch Title Updated.')

    # Get in touch text

    get_in_touch_text_info = get_info_page(db=db, type_info='get_in_touch_text')
    get_in_touch_text_form = GetInTouchText(
        text=get_in_touch_text_info
    )

    if get_in_touch_text_form.submit_get_in_touch_text.data and get_in_touch_text_form.validate():
        text = get_in_touch_text_form.text.data
        db.add_page_info(info_type='get_in_touch_text', value=text)

        flash('Get In Touch Text Updated')

    return render_template('page-info.html', main_title_form=main_title_form, header_img_form=header_img_form,
                           main_text_form=main_text_form, get_in_touch_title_form=get_in_touch_title_form,
                           get_in_touch_text_form=get_in_touch_text_form)


@app.route('/admin/add-work', methods=['GET', 'POST'])
@login_required
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


@app.route('/admin/add-social', methods=['GET', 'POST'])
@login_required
def add_social():
    form = SocialNetwork()
    if form.validate_on_submit():
        social_network_name = form.name.data
        social_network_url = form.url.data

        db.add_social(name=social_network_name, url=social_network_url)
        flash('Social network added')
        return redirect(url_for('personal'))

    return render_template('add-social.html', form=form)


@app.route('/admin/social/edict/<social_id>', methods=['GET', 'POST'])
@login_required
def social_edit(social_id):
    social_network = db.get_social(social_id)
    form = SocialNetwork(
        name=social_network.social_network,
        url=social_network.link
    )

    if form.submit_social.data and form.validate():
        name = form.name.data
        url = form.url.data
        db.add_social(name=name, url=url, social_id=social_network.id)

        flash('Social Network Updated.')
        return redirect(url_for('personal'))

    if request.method == 'POST' and 'social_id' in request.form:
        db.delete_social(social_network=social_network)
        flash('Social Network Deleted')
        return redirect(url_for('personal'))

    return render_template('add-social.html', form=form, social_id=social_network.id)


@app.route('/admin/work/edit/<work_id>', methods=['GET', 'POST'])
@login_required
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


@app.errorhandler(404)
def custom_404(error):
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=False)



