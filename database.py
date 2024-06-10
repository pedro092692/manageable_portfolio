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
    photo_profile_url: Mapped[str] = mapped_column(String(1000), nullable=False)
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


