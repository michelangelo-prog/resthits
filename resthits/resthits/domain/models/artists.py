from resthits.app.rest import db

from .behaviors import CreateAtMixin, IdMixin


class Artist(IdMixin, CreateAtMixin, db.Model):

    __tablename__ = "artists"

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
