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


class PageInfo(db.model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(250), nullable=False)
    value: Mapped[str] = mapped_column(String(250), nullable=False)