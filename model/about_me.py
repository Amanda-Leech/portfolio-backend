from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as ma

from db import db

class About_me(db.Model):
    __tablename__ = "About_me"
    about_me_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    about_name = db.Column(db.String(), nullable=False, unique=True)
    about_info = db.Column(db.String(), nullable=False, unique=True)
    active = db.Column(db.Boolean(), nullable=False, default=True)

    def __init__(self, about_name, about_info, active=True):
        self.about_name = about_name
        self.about_info = about_info
        self.active = active

    def get_new_about():
        return About_me("", "", True)


class AboutSchema(ma.Schema):
    class Meta:
        fields = ['about_me_id', 'about_name', 'about_info', 'active']


about_schema = AboutSchema()
abouts_schema = AboutSchema(many=True)
