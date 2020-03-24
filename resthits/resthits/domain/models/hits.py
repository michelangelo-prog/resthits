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

    @validates("title")
    def validate_title(self, key, value):
        if not value:
            raise ValidationError("Field 'title' not provided.")
        return value

    def __init__(self, *args, **kwargs):
        if not "title_url" in kwargs:
            kwargs["title_url"] = slugify(kwargs.get("title"))
        super().__init__(*args, **kwargs)

    @classmethod
    def get_twenty_recent_hits(cls):
        return cls.query.order_by(cls.created_at.desc()).limit(20).all()

    @classmethod
    def get_hit_by_title_url(cls, title_url):
        return cls.query.filter_by(title_url=title_url).one_or_none()

    @classmethod
    def add_hit_from_json_data(cls, json):
        hit = cls(artist_id=json.get("artistId"), title=json.get("title"))
        cls._add_object_to_db(hit)
        return hit

    @classmethod
    def update_hit_by_title_url_from_json_data(cls, title_url, json_data):
        hit = cls.get_hit_by_title_url(title_url)
        if hit:
            hit.artist_id = json_data["artistId"]
            hit.title = json_data["title"]
            hit.title_url = json_data["titleUrl"]
            cls._commit_db()
            return hit
        return None

    @classmethod
    def delete_hit_by_title_url(cls, title_url):
        hit = cls.get_hit_by_title_url(title_url)
        if hit:
            cls._delete_object_from_db(hit)
            return True
        return

    @classmethod
    def _commit_db(cls):
        db.session.commit()

    @classmethod
    def _add_object_to_db(cls, obj):
        db.session.add(obj)
        cls._commit_db()

    @classmethod
    def _delete_object_from_db(cls, obj):
        db.session.delete(obj)
        cls._commit_db()
