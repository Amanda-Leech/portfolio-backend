from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as ma

from db import db


class Resume(db.Model):
    __tablename__ = "Resume"
    resume_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    resume_date = db.Column(db.String(), nullable=False, unique=True)
    resume_info = db.Column(db.String(), nullable=False, unique=True)
    active = db.Column(db.Boolean(), nullable=False, default=True)

    def __init__(self, resume_date, resume_info, active=True):
        self.resume_date= resume_date
        self.resume_info = resume_info
        self.active = active

    def get_new_resumee():
        return Resume("", "", True)


class ResumeSchema(ma.Schema):
    class Meta:
        fields = ['resume_id','resume_date','resume_info', 'active']


resume_schema = ResumeSchema()
resumes_schema = ResumeSchema(many=True)
