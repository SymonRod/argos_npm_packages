#!/usr/bin/env python3

from fileinput import filename
from sqlalchemy import Column, String, MetaData , Integer, create_engine, ForeignKey, false
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from os import path
import json

file_path = '/home/srodino/scripts/npmVersionVuetify/lastKnown.json'
db_path = 'sqlite:////home/srodino/scripts/npmVersionVuetify/npmVuetifyVersion.db'


Base = declarative_base()

# Path to the database file
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


Session = sessionmaker(bind=engine)

session = Session()
query = session.query(Packages).all()


new_stuff = False
whats_new = {}

if path.exists(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
        for package in query:
            for item in data:
                if package.id == item['id']:
                    for version in session.query(Versions).filter(Versions.package_id == package.id).all():
                        for item_version in item["versions"]:
                            if version.tag == item_version["tag"]:
                                if version.version != item_version["version"]:
                                    new_stuff = True

                                    if package.id in whats_new:
                                        whats_new[package.id]["news"].append({"old_version": item_version["version"],"new_version":version.version, "tag": version.tag})
                                    else:
                                        whats_new[package.id] = {"name": package.name, "url": package.url, "news": [{"old_version": item_version["version"],"new_version":version.version, "tag": version.tag}]}
else:
    with open(file_path,"w") as json_file:
        data = []
        query = session.query(Packages).all()
        for package in query:
            temp_data = {
                "id": package.id,
                "name": package.name,
            }
            temp_data["versions"] = []
            for version in session.query(Versions).filter(Versions.package_id == package.id).all():
                temp_data["versions"].append({"tag": version.tag, "version": version.version})
            
            data.append(temp_data)

        json_file.write(json.dumps(data, indent=4))    


if new_stuff:
    print("🚀🎉    New stuff    🎉🚀")
else:
    print("Packages")
print("---")

for package in query:
    print(package.name)

    for version in session.query(Versions).filter(Versions.package_id == package.id).all():
        print("--" + version.version + " - " + version.tag)

for package in whats_new:
    print("---")
    print("New stuff for "+whats_new[package]["name"]+" 🎉🎉")
    for new in whats_new[package]["news"]:
        print("--" + new["old_version"] + " -> " + new["new_version"] + " - " + new["tag"])

if new_stuff:
    print(" --- ")
    print(f"👌 Clear notifications | bash='rm {file_path}' terminal=false refresh=true")
    