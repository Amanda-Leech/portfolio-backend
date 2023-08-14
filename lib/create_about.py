# from flask_bcrypt import generate_password_hash
from db import db
from model.about import About

def create_about():
    print("Querying for About Me...")

    about_data = db.session.query(About).filter(About.about_title == 'Amanda').first()

    if about_data == None:
        print("About Me not found! Creating one...")
        about_title = 'Amanda'
        about_info = 'About info goes here...'
        active = True

        record = About(about_title, about_info, active)

        db.session.add(record)
        db.session.commit()

    else:
        print("About Me found!")
