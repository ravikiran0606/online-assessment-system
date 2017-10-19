# coding: utf-8
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from db_create import Base


# Base = declarative_base()
metadata = Base.metadata


class BigQuestion(Base):
    __tablename__ = 'BigQuestion'

    q_id = Column(Integer, primary_key=True)
    q_desc = Column(String(100))
    keywords = Column(String(100))
    mark = Column(Integer)

    def __init__(self,q_id,q_desc,keywords,mark):
        self.q_id = q_id
        self.q_desc = q_desc
        self.keywords = keywords
        self.mark = mark


class Objective(Base):
    __tablename__ = 'Objective'

    q_id = Column(Integer, primary_key=True)
    q_desc = Column(String(100))
    choice1 = Column(String(30), nullable=False)
    choice2 = Column(String(30), nullable=False)
    choice3 = Column(String(30), nullable=False)
    c_choice = Column(Integer, nullable=False)

    def __init__(self,q_id,q_desc,choice1,choice2,choice3,c_choice):
        self.q_id = q_id
        self.q_desc = q_desc
        self.choice1 = choice1
        self.choice2 = choice2
        self.choice3 = choice3
        self.c_choice = c_choice

class Result(Base):
    __tablename__ = 'Result'

    test_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, primary_key=True, nullable=False)
    marks = Column(Integer)

    def __init__(self,test_id,user_id,marks):
        self.test_id = test_id
        self.user_id = user_id
        self.marks = marks


class Test(Base):
    __tablename__ = 'Test'

    test_id = Column(Integer, primary_key=True)
    test_name = Column(String(30), nullable=False)
    total_marks = Column(Integer)
    subject = Column(String(30))
    obj1 = Column(Integer)
    obj2 = Column(Integer)
    obj3 = Column(Integer)
    obj4 = Column(Integer)
    obj5 = Column(Integer)
    big1 = Column(Integer)
    big2 = Column(Integer)

    def __init__(self,test_id,test_name,total_marks,subject,obj1,obj2,obj3,obj4,obj5,big1,big2):
        self.test_id = test_id
        self.test_name = test_name
        self.total_marks = total_marks
        self.subject = subject
        self.obj1 = obj1
        self.obj2 = obj2
        self.obj3 = obj3
        self.obj4 = obj4
        self.obj5 = obj5
        self.big1 = big1
        self.big2 = big2



class User(Base):
    __tablename__ = 'User'

    name = Column(String(30), nullable=False)
    email_id = Column(String(30), nullable=False, unique=True)
    user_id = Column(Integer, primary_key=True)
    password = Column(String(30), nullable=False)
    user_type = Column(String(30), nullable=False)

    def __init__(self,name,email_id,user_id,password,user_type):
        self.name = name
        self.email_id = email_id
        self.user_id = user_id
        self.password = password
        self.user_type = user_type

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return self.user_id  # python 2
        except NameError:
            return self.user_id  # python 3
