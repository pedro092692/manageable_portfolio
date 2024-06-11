from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_login import UserMixin
import os


# Create database
class Base(DeclarativeBase):
    pass


# Create Extension
db = SQLAlchemy(model_class=Base)


# Create Tables

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(250), nullable=False)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    password: Mapped[str] = mapped_column(String(500), nullable=False)


class SocialNetwork(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    social_network: Mapped[str] = mapped_column(String(250), nullable=False)
    link: Mapped[str] = mapped_column(String(250), nullable=False)


class Work(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    text_info: Mapped[str] = mapped_column(String(500), nullable=False)
    image_url: Mapped[str] = mapped_column(String(250), nullable=False)
    work_url: Mapped[str] = mapped_column(String(250), nullable=False)


class PageInfo(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(250), nullable=False)
    value: Mapped[str] = mapped_column(String(250), nullable=False)


class Database:

    def __init__(self, app):
        self.db = db
        self.app = app

        # Database init
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', 'sqlite:///portfolio.db')
        self.db.init_app(self.app)

    def create_tables(self):
        with self.app.app_context():
            self.db.create_all()

    def create_work(self, title, text_info, image_url, work_url):
        new_work = Work(
            title=title,
            text_info=text_info,
            image_url=image_url,
            work_url=work_url
        )
        self.db.session.add(new_work)
        self.db.session.commit()
        return new_work

    def get_all_works(self):
        all_works = self.db.session.execute(self.db.select(Work).order_by(Work.title)).scalars().all()
        return all_works

    def get_work(self, work_id):
        work = self.db.get_or_404(Work, work_id)
        return work

    def edit_work(self, work: Work, title, text_info, img_url, work_url):

        work.title = title
        work.text_info = text_info
        work.image_url = img_url
        work.work_url = work_url

        self.db.session.commit()

    def delete_work(self, work: Work):
        self.db.session.delete(work)
        self.db.session.commit()

    def check_page_info_type(self, info_type):
        info = self.db.session.execute(self.db.select(PageInfo).filter(PageInfo.type == info_type)).scalars().first()
        return info

    def add_page_info(self, info_type, value):
        # check if exist previous info
        info = self.check_page_info_type(info_type)
        if info:
            info.value = value
            self.db.session.commit()
        else:
            new_info = PageInfo(
                type=info_type,
                value=value
            )
            self.db.session.add(new_info)
            self.db.session.commit()
            return new_info

    def add_social(self, name, url, social_id=None):
        if social_id:
            social_network = self.get_social(social_id)
            if social_network:
                social_network.social_network = name
                social_network.link = url
                self.db.session.commit()
        else:
            new_social = SocialNetwork(
                social_network=name,
                link=url
            )

            self.db.session.add(new_social)
            self.db.session.commit()

            return new_social

    def all_social(self):
        all_social = self.db.session.execute(self.db.select(SocialNetwork).order_by(SocialNetwork.social_network)).scalars().all()
        return all_social

    def get_social(self, social_id):
        social_network = self.db.get_or_404(SocialNetwork, social_id)
        return social_network

    def delete_social(self, social_network: SocialNetwork):
        self.db.session.delete(social_network)
        self.db.session.commit()

    def check_user(self, email=''):
        if email:
            user = User.query.filter_by(email=email).first()
            return user
        else:
            users = self.db.session.execute(self.db.select(User)).scalars().all()
            return users

    def create_user(self, email, name, password):
        new_user = User(
            email=email,
            name=name,
            password=password
        )
        self.db.session.add(new_user)
        self.db.session.commit()

        return new_user

    def get_user(self, user_id):
        return self.db.get_or_404(User, user_id)




