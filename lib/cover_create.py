from flask_bcrypt import generate_password_hash
from db import db
from model.cover import Cover

def create_cover():
    print("Querying for Cover Letter...")

    cover_data = db.session.query(Cover).filter(Cover.cover_title == 'Amanda').first()

    if cover_data == None:
        print("Cover Letter not found! Creating one...")
        cover_title = 'Amanda'
        cover_info = 'Cover letter goes here...'
        active = True

        record = Cover(cover_title, cover_info, active)

        db.session.add(record)
        db.session.commit()

    else:
        print("Cover Letter found!")
