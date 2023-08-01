from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as ma
from db import db
from .user import UserSchema


class Auth(db.Model):
    __tablename__ = "Auth"
    auth_token = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('User.user_id'), nullable=False)
    expiration = db.Column(db.DateTime, nullable=False)
    user = db.relationship("User", back_populates="auth")

    def __init__(self, user_id, expiration):
        self.user_id = user_id
        self.expiration = expiration


class AuthTokenSchema(ma.Schema):
    class Meta:
        fields = ['auth_token', 'user', 'expiration']

    user = ma.fields.Nested(UserSchema(only=("role", "user_id", "active")))


auth_token_schema = AuthTokenSchema()