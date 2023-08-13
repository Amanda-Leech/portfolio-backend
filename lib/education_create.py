from db import db
from model.education import Education

def create_education():
    print("Querying for Education info...")

    education_data = db.session.query(Education).filter(Education.certificate == 'Associates of general education').first()

    if education_data == None:
        print("Education info not found! Creating one...")
        certificate = 'Associates of general education'
        school_name = 'Weber'
        date_obtained = "2012"
        active = True

        record = Education(certificate, school_name, date_obtained, active)

        db.session.add(record)
        db.session.commit()

        certificate = 'Front-end Certificate'
        school_name = 'DevPipeline'
        date_obtained = "2022"
        active = True

        record = Education(certificate, school_name, date_obtained, active)

        db.session.add(record)
        db.session.commit()

    else:
        print("Education info found!")
