from marshmallow import ValidationError
from sqlalchemy.orm import validates

from resthits.app.rest import db

from .behaviors import CreateAtMixin, IdMixin


class Artist(IdMixin, CreateAtMixin, db.Model):

    __tablename__ = "artists"

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    @validates("first_name")
    def validate_first_name(self, key, value):
        if not key or not value:
            raise ValidationError("Field 'first_name' not provided.")
        return value

    @validates("last_name")
    def validate_last_name(self, key, value):
        if not key or not value:
            raise ValidationError("Field 'last_name' not provided.")
        return value
