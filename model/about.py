from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as ma

from db import db

class About(db.Model):
    __tablename__ = "About"
    about_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    about_title = db.Column(db.String(), nullable=False, unique=True)
    about_info = db.Column(db.String(), nullable=False, unique=True)
    active = db.Column(db.Boolean(), nullable=False, default=True)

    def __init__(self, about_title, about_info, active=True):
        self.about_title = about_title
        self.about_info = about_info
        self.active = active

    def get_new_about():
        return About("", "", True)


class AboutSchema(ma.Schema):
    class Meta:
        fields = ['about_id', 'about_title', 'about_info', 'active']


about_schema = AboutSchema()
abouts_schema = AboutSchema(many=True)
