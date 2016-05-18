from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from config import config
import os

DB_URL = config[os.getenv('FLASK_CONFIG') or 'default'].SQLALCHEMY_DATABASE_URI
Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=create_engine(DB_URL))
session = scoped_session(Session)
