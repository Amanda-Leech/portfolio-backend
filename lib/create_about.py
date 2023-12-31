# from flask_bcrypt import generate_password_hash
from db import db
from model.about import About

def create_about():
    print("Querying for About Me...")

    about_data = db.session.query(About).filter(About.about_title == 'Amanda').first()

    if about_data == None:
        print("About Me not found! Creating one...")
        about_title = 'Amanda'
        about_info = "Result-oriented and strategy-driven Junior developer with years of demonstrable success in software design and coding. I have a strong background rooted in reporting directly to the development manager and helping with all software coding and design functions. Responsible for working on small bug fixes while monitoring the technical performance of internal systems. I am also recognized as an expert whose expertise lies in maintaining an awareness of developing technology and industry trends and incorporating them into operations and activities. I have been instrumental in report writing and performing development tests. Furthermore, I pride myself on being a strategic thinker with a solution-oriented mindset while assessing the root cause of problems to provide exceptional solutions."  

 
        active = True

        record = About(about_title, about_info, active)

        db.session.add(record)
        db.session.commit()

    else:
        print("About Me found!")
