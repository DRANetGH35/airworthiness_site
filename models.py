from flask_login import UserMixin
from typing import List
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime

from extensions import db

class User(UserMixin, db.Model):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    email: Mapped[str] = mapped_column(String(1000))
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, nullable=False)
    planes: Mapped[List["Plane"]] = relationship(back_populates="user")

    @classmethod
    def exists(cls, username: str) -> bool:
        return cls.query.filter_by(name=username).first() is not None

    @classmethod
    def get_by_username(cls, username: str):
        return cls.query.filter_by(name=username).first()

    @classmethod
    def get(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

class Plane(db.Model):
    __tablename__ = "plane_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(1000))
    user: Mapped[User] = relationship("User", back_populates="planes")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_table.id"))