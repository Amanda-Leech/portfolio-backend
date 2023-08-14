from db import db
from model.education import Education

def create_education():
    print("Querying for Education info...")

    education_data = db.session.query(Education).filter(Education.date_obtained == '2014').first()


    if education_data == None:
        print("Education not found! Creating one...")
        school_name = "Weber"
        certificate = "Assiciate of science general education"
        date_obtained = "2014"
        active = True

        record = Education(school_name, certificate, date_obtained, active)

        db.session.add(record)
        db.session.commit()

        school_name = "DevPipeline"
        certificate = "Foundations Web Development"
        date_obtained = "2014"
        active = True

        record = Education(school_name, certificate, date_obtained, active)

        db.session.add(record)
        db.session.commit()
    else:
        print("Education info found!")
