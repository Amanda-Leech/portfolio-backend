from db import db
from model.message import Message

def create_message():
    print("Querying for Message info...")

    message_date = db.session.query(Message).filter(Message.message_name == 'Amanda').first()

    if message_date == None:
        print("Message info not found! Creating one...")
        message_name = 'Amanda'
        message_email = 'Leechamanda85@gmail.com'
        message_subject = "Good morning"
        message = "Hello, how is your day going?"
        active = True

        record = Message(message_name, message_email, message_subject, message, active)

        db.session.add(record)
        db.session.commit()

        message_name = 'Name'
        message_email = 'Email address'
        message_subject = "Subject"
        message = "Message body"
        active = True

        record = Message(message_name, message_email, message_subject, message, active)

        db.session.add(record)
        db.session.commit()

    else:
        print("Message info found!")
