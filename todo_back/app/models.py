# このフファイはORMモデルのクラスについて責任を持つ

from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)


class tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    done  = Column(Boolean)
    uid = Column(Integer, ForeignKey=True)