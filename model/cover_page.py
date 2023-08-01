from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as ma

from db import db


class Cover_page(db.Model):
    __tablename__ = "Cover_page"
    cover_page_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    cover_info = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)

    def __init__(self, cover_info, active=True):
        self.cover_info = cover_info
        self.active = active

    def get_new_cover():
        return Cover_page("", True)


class CoverSchema(ma.Schema):
    class Meta:
        fields = ['cover_page_id', 'cover_info', 'active']


cover_schema = CoverSchema()
covers_schema = CoverSchema(many=True)
