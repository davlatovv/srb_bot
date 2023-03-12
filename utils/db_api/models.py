from utils.db_api.database import db
from sqlalchemy import (Column, Integer, BigInteger, Sequence,
                        String, TIMESTAMP, Boolean, JSON, ForeignKey, DateTime)
from sqlalchemy.orm import relationship
from sqlalchemy import sql
from sqlalchemy import Column, Integer, String, create_engine


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_created = Column(DateTime(timezone=True), server_default=db.func.now())
    user_id = Column(BigInteger)
    referral = Column(String(100))
    ref_id = Column(String(100))
    count_ref = Column(String(7))
    language = Column(String(2))
    full_name = Column(String(50))
    nickname = Column(String(50), unique=True)
    age = Column(String(100))
    gender = Column(String(50))
    photo = Column(String(100))
    school = Column(String(10))
    classroom = Column(String(50))
    subscribe = Column(Boolean, default=False,  nullable=False)
    time_start = Column(String(25))
    time_end = Column(String(25))
    region = Column(String(50))
    district = Column(String(100))
    like = Column(BigInteger, default=0)
    ban = Column(Boolean, default=False)
    query: sql.Select


class Region(db.Model):
    __tablename__ = "region"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    language = Column(String(2))
    query: sql.Select


class District(db.Model):
    __tablename__ = "district"
    id = Column(Integer, primary_key=True, autoincrement=True,)
    name = Column(String(100))
    language = Column(String(2))
    region_id = Column(Integer, ForeignKey('region.id'))
    region = relationship("Region")
    query: sql.Select


class School(db.Model):
    __tablename__ = "school"
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(50))
    district_id = Column(Integer, ForeignKey('district.id'))
    district = relationship("District")
    query: sql.Select


class Classroom(db.Model):
    __tablename__ = "classroom"
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(50))
    school_id = Column(Integer, ForeignKey('school.id'))
    school = relationship("School")
    query: sql.Select


class Quiz(db.Model):
    __tablename__ = "quiz"
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String(250))
    language = Column(String(2))
    classes = Column(String(2))
    query: sql.Select


class Finance(db.Model):
    __tablename__ = "finance"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    full_name = Column(String(255))
    amount = Column(BigInteger)
    type = Column(String(10))
    query: sql.Select


class Subscribe(db.Model):
    __tablename__ = "subscribe"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    other_id = Column(BigInteger)
    other_photo = Column(String(150))
    other_name = Column(String(100))
    other_lang = Column(String(2))
    question = Column(String(100))
    query: sql.Select






