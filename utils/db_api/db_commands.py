import logging
from datetime import datetime

from aiogram import types, Bot
from typing import List

from .database import db
from sqlalchemy import and_, sql, not_, create_engine, select, distinct, except_, func
from .models import User, Region, District, School, Classroom, Quiz
from sqlalchemy.orm import Session, session
from data.config import POSTGRES_URI
import random
from dateutil.relativedelta import relativedelta


class DBCommands:

    async def get_user(self, user_id) -> User:
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user
    async def get_all(self):
        users = await select(User).gino.all()
        return users

    async def ban_unbun(self, user, ban=bool):
        user = await self.get_user(user)
        await user.update(ban=ban).apply()

    async def check_ban(self, user_id):
        user = await User.query.where(and_(User.user_id == user_id, User.ban == True)).gino.first()
        if user:
            return False

    async def add_new_user(self, ref=None, refferal=None) -> User:
        user = types.User.get_current()
        new_user = User()
        if ref != None:
            new_user.user_id = user.id
            new_user.ref_id = ref
            new_user.referral = refferal
            await new_user.create()
        else:
            new_user.user_id = user.id
            new_user.referral = refferal
            await new_user.create()
        return new_user

    async def set_language(self, language):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        await user.update(language=language).apply()

    async def count_users(self):
        total = await db.func.count(User.user_id).gino.scalar()
        return total

    async def class_rating(self, school, clas):
        query = select([User.like]).where(and_(User.like == db.select([db.func.max(User.like)]), User.school == school, User.classroom == clas)).limit(3)
        result = await query.gino.all()
        return result

    async def all_rating(self):
        query = select([User.like]).where(
            User.like == db.select([db.func.max(User.like)])
        ).limit(3)
        result = await query.gino.all()
        return result

    async def like(self, like):
        user = await User.query.where(User.like == like).gino.first()
        return user

    async def school_rating(self, school):
        query = select([User.like]).where(and_(User.like == db.select([db.func.max(User.like)]), User.school == school)).limit(3)
        result = await query.gino.all()
        return result

    async def get_classmates(self, room):
        classmates = await User.query.where(User.classroom == room).gino.all()
        count = [i for i in classmates]
        if len(count) > 1:
            return True
        else:
            return False

    async def count_rooms(self, room):
        rooms = await select([User.classroom]).where(User.classroom == room).gino.all()
        if len(rooms) >= 2:
            return rooms
        else:
            return 0
    async def get_classmates_for_quiz1(self, school, number):
        classmates = await select([User.classroom]).distinct().where(and_(User.school == school, User.classroom.like(f"%{number}%"))).gino.all()
        return classmates

    async def get_regions(self, lang) -> List[Region]:
        reg = await Region.query.where(Region.language == lang).gino.all()
        return reg

    async def get_district(self, region) -> List[District]:
        dist = await District.query.where(and_(Region.name == region, Region.id == District.region_id)).gino.all()
        return dist

    async def get_school(self, district) -> List[School]:
        school = await School.query.where(and_(District.name == district, District.id == School.district_id)).gino.all()
        return school

    async def choice_school(self, number):
        school = await School.query.where(School.number == number).gino.first()
        if school == None:
            return False
        return school.number

    async def get_classroom(self, school) -> List[Classroom]:
        classroom = await Classroom.query.where(and_(School.number == school, School.id == Classroom.school_id)).gino.all()
        return classroom

    async def set_full_name(self, full_name):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        await user.update(full_name=full_name).apply()

    async def set_nickname(self, nickname):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        await user.update(nickname=nickname).apply()

    async def set_age(self, age):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        await user.update(age=age).apply()

    async def set_gender(self, gender):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        await user.update(gender=gender).apply()

    async def set_school(self, school):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        await user.update(school=school).apply()

    async def set_district(self, district):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        await user.update(district=district).apply()

    async def set_region(self, region):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        await user.update(region=region).apply()

    async def set_classroom(self, classroom):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        await user.update(classroom=classroom).apply()

    async def set_subscribe(self, subscribe):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        await user.update(subscribe=subscribe).apply()

    async def set_subscribe2(self, subscribe, user_id):
        user = await self.get_user(user_id)
        await user.update(subscribe=subscribe).apply()

    async def start_premium(self, time_start):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        await user.update(time_start=time_start).apply()
        time_end = datetime.strptime(time_start, '%Y-%m-%d %H:%M:%S') + relativedelta(months=1)
        await user.update(time_end=str(time_end).split(' ')[0]).apply()

    async def set_photo(self, photo):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        await user.update(photo=photo).apply()

    async def get_premium(self, full_name) -> List[User]:
        user = await User.query.where(and_(User.full_name == full_name, User.subscribe == True)).gino.first()
        if user != None:
            return user.user_id

    async def get_all_subscribers(self):
        users = await User.query.where(User.subscribe == True).gino.all()
        return users

    async def get_simple(self, full_name) -> List[User]:
        user = await User.query.where(and_(User.full_name == full_name, User.subscribe == False)).gino.first()
        if user != None:
            return user.user_id

    async def set_count_ref(self):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        count = await User.query.where(User.ref_id == str(user_id)).gino.scalar()
        await user.update(count_ref=str(count)).apply()


    async def quest(self, school, room, user):
        users = await User.query.where(and_(User.school == school, User.classroom == room, User.user_id != user)).gino.all()
        for i in random.sample(users, len(users)):
            return i

    async def plus_like(self, user_id):
        user = await self.get_user(user_id)
        like = user.like
        await user.update(like=like+1).apply()

    async def get_questions(self, lang, number):
        quiz = await select(Quiz).where(and_(Quiz.language == lang, Quiz.classes == number)).gino.all()
        return quiz

    async def get_people(self, school, number):
        user_id = types.User.get_current().id
        classmates = await select(User).where(and_(User.school == school, User.classroom == number, User.user_id != user_id)).gino.all()
        return classmates




