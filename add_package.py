if __name__ == "__main__":
    from db import *

    package_complete = input("Please input the package url from npmjs.com (example: https://www.npmjs.com/package/@vuetify/nightly): ")

    package_name = package_complete.split("/package/")[-1]
    

    Session = sessionmaker(bind=engine)
    session = Session()
    package = Packages(name=package_name, url=package_complete)

    session.add(package)
    session.commit()

    import getVersionFromNpm


