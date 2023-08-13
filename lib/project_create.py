from db import db
from model.project import Project

def create_project():
    print("Querying for Project info...")

    project_date = db.session.query(Project).filter(Project.project_title == 'Cupcake ecomerce website').first()

    if project_date == None:
        print("Project info not found! Creating one...")
        project_title = 'Cupcake ecomerce website'
        project_url = 'website'
        git_url = "https://github.com/Amanda-Leech/cupcake_typescript"
        project_info = "Website my for my son to sell his baked goods."
        active = True

        record = Project(project_title, project_url, git_url, project_info, active)

        db.session.add(record)
        db.session.commit()

        project_title = 'Axolotl web scraper'
        project_url = 'none'
        git_url = "https://github.com/Amanda-Leech/web_scraper_axolotl"
        project_info = "scrapes info from a webpage on Axolotls"
        active = True

        record = Project(project_title, project_url, git_url, project_info, active)

        db.session.add(record)
        db.session.commit()

    else:
        print("Project info found!")
