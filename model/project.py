from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as ma

from db import db


class Project(db.Model):
    __tablename__ = "Application"
    project_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    project_title = db.Column(db.String(), nullable=False, unique=True)
    project_url = db.Column(db.String())
    git_url = db.Column(db.String())
    project_info = db.Column(db.String())
    active = db.Column(db.Boolean(), nullable=False, default=True)

    def __init__(self, project_title, project_url, git_url, project_info, active=True):
        self.project_title = project_title
        self.project_url = project_url
        self.git_url= git_url
        self.project_info = project_info
        self.active = active

    def get_new_project():
        return Project("", "", "", "", True)


class ProjectSchema(ma.Schema):
    class Meta:
        fields = ['project_id', 'project_title', 'project_url', 'git_url', 'project_info', 'active']


project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)
