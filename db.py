#!/usr/bin/env python3

from sqlalchemy import Column, String, MetaData , Integer, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

db_path = 'sqlite:////home/srodino/scripts/npmVersionVuetify/npmVuetifyVersion.db'

Base = declarative_base()

engine = create_engine(db_path)

class Versions(Base):
    __tablename__ = 'versions'
    id = Column(Integer, primary_key=True)
    version = Column(String(30))
    downloads = Column(String(30))
    tag = Column(String(60))
    package_id = Column(Integer, ForeignKey('packages.id'))
    
class Packages(Base):
    __tablename__ = 'packages'
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    url = Column(String(100))

Base.metadata.create_all(engine)