#!/usr/bin/python3

from db import *
import subprocess

Session = sessionmaker(bind=engine)

session = Session()

query = session.query(Packages).all()

for package in query:
    command = "npm dist-tag ls " + package.name
    output = subprocess.check_output(command, shell=True)
    output = output.decode("utf-8")
    output = output.split("\n")
    for line in output:
        
        line = line.split(": ")
        
        if len(line) < 2:
            break
        tag_name = line[0]
        version = line[1]
        update_query = session.query(Versions).filter(Versions.package_id == package.id, Versions.tag == tag_name).first()
        
        if update_query is None:
            update_query = Versions(package_id=package.id, tag=tag_name, version=version)
            session.add(update_query)
            session.commit()

        if update_query:
            update_query.version = version
            session.commit()

