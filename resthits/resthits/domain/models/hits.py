from marshmallow import ValidationError
from slugify import slugify
from sqlalchemy.orm import backref, relationship, validates

from resthits.app.rest import db

from .artists import Artist
from .behaviors import CreateAtMixin, IdMixin, UpdateAtMixin


class Hit(IdMixin, CreateAtMixin, UpdateAtMixin, db.Model):

    __tablename__ = "hits"

    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    title_url = db.Column(db.String(300), nullable=False)

    artist = relationship(Artist, backref=backref("hits", uselist=True))

    def __init__(self, *args, **kwargs):
        if not "title_url" in kwargs:
            kwargs["title_url"] = slugify(kwargs.get("title"))
        super().__init__(*args, **kwargs)

    @validates("title")
    def validate_title(self, key, value):
        if not value:
            raise ValidationError("Field 'title' not provided.")
        return value
