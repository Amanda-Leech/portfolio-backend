from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as ma

from db import db


class Education(db.Model):
    __tablename__ = "Education"
    education_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    school_name = db.Column(db.String())
    certificate = db.Column(db.String(), nullable=False, unique=True)
    date_obtained = db.Column(db.String())
    active = db.Column(db.Boolean(), nullable=False, default=True)

    def __init__(self, school_name, certificate, date_obtained, active=True):
        self.school_name = school_name
        self.certificate = certificate
        self.date_obtained = date_obtained
        self.active = active

    def get_new_education():
        return Education("", "", "", True)


class EducationSchema(ma.Schema):
    class Meta:
        fields = ['education_id', 'school_name', 'certificate', 'date_obtained', 'active']


education_schema = EducationSchema()
educations_schema = EducationSchema(many=True)
