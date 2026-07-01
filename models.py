from flask_login import UserMixin
from typing import List
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, func, Float, select
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
    verification_code: Mapped[str] = mapped_column(String(1000))
    planes: Mapped[List["Plane"]] = relationship(back_populates="user")
    hobbs_time: Mapped[float] = mapped_column(Float)

    def updateHobbsTime(self):
        total = 0
        for plane in self.planes:
            for time_entry in plane.timetable:
                total += time_entry.tach_time
        self.hobbs_time = total * 1.2

    @classmethod
    def exists(cls, username: str) -> bool:
        return cls.query.filter_by(name=username).first() is not None

    @classmethod
    def get_by_username(cls, username: str):
        return cls.query.filter_by(name=username).first()

    @classmethod
    def get(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    def is_verified(self):
        return self.verified

    def set_verified(self, verified: bool):
        self.verified = verified
        db.session.commit()

class Plane(db.Model):
    __tablename__ = "plane_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(1000))
    user: Mapped[User] = relationship("User", back_populates="planes")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_table.id"))
    timetable: Mapped[List["TimeEntry"]] = relationship(back_populates="plane")
    maintenance_items: Mapped[List["MaintenanceEntry"]] = relationship(back_populates="plane")
    engines: Mapped[List["Engine"]] = relationship(back_populates="plane", order_by="Engine.created")
    initial_tach_hours: Mapped[float] = mapped_column(Float, nullable=True)
    tach_hours: Mapped[float] = mapped_column(Float)

    def get_latest_engine(cls):
        stmt = (
            select(Engine)
            .join(Plane.engines)
            .where(Plane.id == cls.id)
            .order_by(Engine.id.desc())
            .limit(1)
        )
        return db.session.scalars(stmt).first()

    def updateTachHours(self):
        total = 0 if self.initial_tach_hours is None else self.initial_tach_hours
        for time_entry in self.timetable:
            total += time_entry.tach_time
        self.tach_hours = total

class Engine(db.Model):
    __tablename__ = "engines_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime)
    plane: Mapped[Plane] = relationship("Plane", back_populates="engines")
    plane_id: Mapped[int] = mapped_column(Integer, ForeignKey("plane_table.id"))
    initial_tach_hours: Mapped[float] = mapped_column(Float, nullable=True)
    tach_hours: Mapped[float] = mapped_column(Float)
    overhauls: Mapped[List["Overhaul"]] = relationship(back_populates="engine", order_by='Overhaul.created')
    time_entries: Mapped[List["TimeEntry"]] = relationship(back_populates="engine")

    def get_latest_overhaul(cls):
        stmt = (
            select(Overhaul)
            .join(Engine.overhauls)
            .where(Engine.id == cls.id)
            .order_by(Overhaul.id.desc())
            .limit(1)
        )
        return db.session.scalars(stmt).first()

    def updateTachHours(self):
        total = 0 if self.initial_tach_hours is None else self.initial_tach_hours
        for time_entry in self.time_entries:
            total += time_entry.tach_time
        self.tach_hours = total

class Overhaul(db.Model):
    __tablename__ = "overhauls_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    engine: Mapped[Engine] = relationship("Engine", back_populates="overhauls")
    engine_id: Mapped[int] = mapped_column(Integer, ForeignKey("engines_table.id"))
    created: Mapped[datetime.datetime] = mapped_column(DateTime)
    initial_tach_hours: Mapped[float] = mapped_column(Float, nullable=True)
    tach_hours: Mapped[float] = mapped_column(Float)
    time_entries: Mapped[List["TimeEntry"]] = relationship(back_populates="overhaul")

    def updateTachHours(self):
        total = 0 if self.initial_tach_hours is None else self.initial_tach_hours
        for time_entry in self.time_entries:
            total += time_entry.tach_time
        self.tach_hours = total

class TimeEntry(db.Model):
    __tablename__ = "time_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime)
    tach_time: Mapped[float] = mapped_column(Float)
    plane: Mapped[Plane] = relationship("Plane", back_populates="timetable")
    plane_id: Mapped[int] = mapped_column(Integer, ForeignKey("plane_table.id"))
    engine: Mapped[Engine] = relationship("Engine", back_populates="time_entries")
    engine_id: Mapped[int] = mapped_column(Integer, ForeignKey("engines_table.id"), nullable=True)
    overhaul: Mapped[Overhaul] = relationship("Overhaul", back_populates="time_entries")
    overhaul_id: Mapped[int] = mapped_column(Integer, ForeignKey("overhauls_table.id"), nullable=True)

class MaintenanceEntry(db.Model):
    __tablename__ = "maintenance_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    maintenance_type: Mapped[str] = mapped_column(String(1000), nullable=True)
    interval: Mapped[bool] = mapped_column(Boolean, nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    tach_last_completed: Mapped[float] = mapped_column(Float, nullable=True)
    date_last_completed: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    interval_hours: Mapped[float] = mapped_column(Float, nullable=True)
    interval_months: Mapped[float] = mapped_column(Float, nullable=True)
    due_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    due_tach: Mapped[float] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(1000))
    plane: Mapped[Plane] = relationship("Plane", back_populates="maintenance_items")
    plane_id: Mapped[int] = mapped_column(Integer, ForeignKey("plane_table.id"))