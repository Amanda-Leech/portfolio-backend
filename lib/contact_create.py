from flask_bcrypt import generate_password_hash
from db import db
from model.contact import Contact

def create_contact():
    print("Querying for Contact Me...")

    contact_data = db.session.query(Contact).filter(Contact.contact_name == 'Amanda_Leech').first()

    if contact_data == None:
        print("Contact not found! Creating one...")
        contact_name = 'Amanda_Leech'
        linked_in = 'https://www.linkedin.com/in/amanda-leech-40b509262/'
        git_hub = 'https://github.com/Amanda-Leech'
        phone = '385-226-2946'
        email = 'Amanda_O_Leech@yahoo.com'
        address = 'American Fork, Utah'

        record = Contact(contact_name, linked_in, git_hub, phone, email, address)

        db.session.add(record)
        db.session.commit()

    else:
        print("Contact Me found!")
