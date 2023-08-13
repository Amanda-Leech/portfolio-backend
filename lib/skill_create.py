from db import db
from model.skill import Skill

def create_skill():
    print("Querying for Skill info...")

    skill_data = db.session.query(Skill).filter(Skill.skill_name == 'Typescript').first()


    if skill_data == None:
        print("Skill not found! Creating one...")
        skill_name = 'Typescript'
        skill_use = 'cupcake ecomerce site'
        active = True

        record = Skill(skill_name, skill_use, active)

        db.session.add(record)
        db.session.commit()

        skill_name = 'Python'
        skill_use = 'Profile website'
        active = True

        record = Skill(skill_name, skill_use, active)

        db.session.add(record)
        db.session.commit()

    else:
        print("Skill info found!")
