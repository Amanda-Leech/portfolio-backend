from flask_bcrypt import generate_password_hash
from db import db
from model.cover import Cover

def create_cover():
    print("Querying for Cover Letter...")

    cover_data = db.session.query(Cover).filter(Cover.cover_title == 'Amanda').first()

    if cover_data == None:
        print("Cover Letter not found! Creating one...")
        cover_title = 'Amanda'
        cover_info = "I am a Junior developer with a solid background in the Technology industry. Responsible for working on small bug fixes while monitoring the technical performance of internal systems. Respected empathetic leader and contributor with the innate ability to inspire confidence at all levels. I am passionate, engaging, and endowed with the knowledge to apply strong analytical thinking skills and proficiency in performing functions like planning, organizing, staffing, directing, and controlling. I possess the knowledge and expertise that will allow me to contribute to the success of your establishment. My experience lies in working and supervising a team. Successfully conceptualizing, developing, and identifying viable software solutions. Over the years, I have gained the necessary skills and knowledge to tackle every problem that comes with this role. Many of my accomplishments enjoyed in previous establishments detailed in my resume resulted from interpreting and implementing quality assurance standards to provide accurate and comprehensive feedback to colleagues. I am a self-motivated, resourceful, and dynamic leader with the ability to create and manage cohesive, productive work teams. With my experience and credentials, I am well prepared to contribute tremendously to the success of your organization. I would enjoy the opportunity to meet with you to discuss how my diverse skills and experience will enable me to make a valuable contribution to your organization. If you are interested in learning more about how I can be an asset to your organization, then I’d be happy to schedule an interview. "
        active = True

        record = Cover(cover_title, cover_info, active)

        db.session.add(record)
        db.session.commit()

    else:
        print("Cover Letter found!")
