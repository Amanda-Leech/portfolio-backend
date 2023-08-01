from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as ma

from db import db


class Skill(db.Model):
    __tablename__ = "Skill"
    skill_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    skill_name = db.Column(db.String(), nullable=False, unique=True)
    skill_use = db.Column(db.String(), nullable=False, unique=True)
    active = db.Column(db.Boolean(), nullable=False, default=True)


    def __init__(self, skill_name, skill_use, active=True):
        self.skill_name = skill_name
        self.skill_use = skill_use
        self.active = active

    def get_new_skill():
        return Skill("", "", True)


class SkillSchema(ma.Schema):
    class Meta:
        fields = ['skill_id','skill_name','skill_use', 'active']


skill_schema = SkillSchema()
skills_schema = SkillSchema(many=True)
