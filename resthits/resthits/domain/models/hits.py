from sqlalchemy.orm import backref, relationship

from resthits.app.rest import db

from .artists import Artist
from .behaviors import CreateAtMixin, IdMixin, UpdateAtMixin


class Hit(IdMixin, CreateAtMixin, UpdateAtMixin, db.Model):

    __tablename__ = "hits"

    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"))
    title = db.Column(db.String(200), nullable=False)
    title_url = db.Column(db.String(300), nullable=False)

    artist = relationship(Artist, backref=backref("hits", uselist=True), nullable=False)
