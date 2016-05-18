from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Cultivation(Base):
    __tablename__ = 'cultivations'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.uid'))
    habit_id = Column(Integer, ForeignKey('habits.id'))
    continuous_days = Column(Integer)
    last_checkin_date = Column(DateTime, default=datetime.utcnow)
    habit = relationship('Habit')
    checkins = relationship('Checkin', backref='cultivation', lazy='dynamic')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True, index=True)
    password = Column(String(32))
    avatar_url = Column(String(128))
    description = Column(String(256))
    gender = Column(String(2))
    token = Column(String(128))
    create_date = Column(DateTime, default=datetime.utcnow)
    device_id = Column(String(64))
    uid = Column(Integer)
    expired_in = Column(DateTime)
    habits = relationship('Cultivation')
    comments = relationship('Comment', backref='user', lazy='dynamic')
    supports = relationship('Support', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username


class Habit(Base):
    __tablename__ = 'habits'
    id = Column(Integer, primary_key=True)
    title = Column(String(32), unique=True, index=True)
    frequency = Column(Integer)
    tags = Column(String(128))
    description = Column(String(256))
    category_id = Column(Integer, ForeignKey('categories.id'))
    
    def __repr__(self):
        return '<Habit %r>' % self.title


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True, index=True)
    habits = relationship('Habit', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category %r>' % self.name


class Checkin(Base):
    __tablename__ = 'checkins'
    id = Column(Integer, primary_key=True)
    cultivation_id = Column(Integer, ForeignKey('cultivations.id'))
    comments = relationship('Comment', backref='checkin', lazy='dynamic')
    supports = relationship('Support', backref='checkin', lazy='dynamic')

    def __repr__(self):
        return '<Checkin %r>' % self.cultivation_id


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(String(256))
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    checkin_id = Column(Integer, ForeignKey('checkins.id'))
    from_user_id = Column(Integer, ForeignKey('users.id'))
    
    def __repr__(self):
        return '<Comment %r' % self.content


class Support(Base):
    __tablename__ = 'supports'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    check_id = Column(Integer, ForeignKey('checkins.id'))
    from_user_id = Column(Integer, ForeignKey('users.id'))
    
    def __repr__(self):
        return '<Support %r>'

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from config import config
    import os
    DB_URI = config[os.getenv('FLASK_CONFIG') or 'default']
    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
