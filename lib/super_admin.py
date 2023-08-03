from flask_bcrypt import generate_password_hash
from db import db
from model.user import User

def create_admin():
    print("Querying for Super Admin user...")

    user_data = db.session.query(User).filter(User.email == 'Amanda_O_Leech@yahoo.com').first()

    if user_data == None:
        print("Super Admin not found! Creating Amanda_O_Leech@yahoo.com user...")
        email = 'Amanda_O_Leech@yahoo.com'
        newpw = input(' Enter a password: ')
        password = newpw
        hashed_password = generate_password_hash(password).decode("utf8")
        active = True
        role = 'admin'

        record = User(email, hashed_password, role, active)

        db.session.add(record)
        db.session.commit()

    else:
        print("super user found!")
