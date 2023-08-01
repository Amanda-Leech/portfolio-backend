from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as ma
from db import db


class User(db.Model):
    __tablename__ = "User"
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False, unique=True)
    role = db.Column(db.String(), default='admin', nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)

    auth = db.relationship('AuthToken', back_populates='user')

    def __init__(self, email, password, role='admin', active=True):
        self.email = email
        self.password = password
        self.role = role
        self.active = active

    def get_new_user():
        return User("", "", "admin", True)


class UserSchema(ma.Schema):
    class Meta:
        fields = ['user_id', 'email', 'role', 'active']


user_schema = UserSchema()
users_schema = UserSchema(many=True)
