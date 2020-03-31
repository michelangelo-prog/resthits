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
    def add_hit_from_json_data(cls, data):
        if Artist.get_by_id(data["artistId"]):
            title_url = cls.get_available_title_url_by_title(data["title"])
            hit = cls(
                artist_id=data["artistId"], title=data["title"], title_url=title_url
            )
            cls._add_object_to_db(hit)
            return hit
        return None

    @classmethod
    def get_available_title_url_by_title(cls, title):
        title_url = slugify(title)
        title_url = cls._set_up_title_url(title_url)
        return title_url

    @classmethod
    def _set_up_title_url(cls, title_url):
        if cls.get_hit_by_title_url(title_url):
            title_url = cls._format_title_url(title_url)
            return cls._set_up_title_url(title_url)
        return title_url

    @classmethod
    def _format_title_url(cls, title_url):
        phrases = title_url.split("-")
        try:
            value = int(phrases[-1])
        except ValueError:
            return "{}-2".format(title_url)
        else:
            phrases[-1] = str(value + 1)
            return "-".join(phrases)

    @classmethod
    def update_hit_by_title_url_from_json_data(cls, title_url, json_data):
        hit = cls.get_hit_by_title_url(title_url)
        artist = Artist.get_by_id(json_data["artistId"])
        if (
            artist
            and hit
            and not cls._title_url_is_available_in_another_artists_songs(
                artist.id, json_data["titleUrl"]
            )
        ):
            hit.artist = artist
            hit.title = json_data["title"]
            if hit.title_url != json_data["titleUrl"]:
                hit.title_url = cls._set_up_title_url(json_data["titleUrl"])
            cls._commit_db()
            return hit
        return None

    @classmethod
    def _title_url_is_available_in_another_artists_songs(cls, artist_id, title_url):
        return (
            True
            if cls.query.filter(
                (cls.artist_id != artist_id) & (cls.title_url == title_url)
            ).first()
            else False
        )

    @classmethod
    def delete_hit_by_title_url(cls, title_url):
        hit = cls.get_hit_by_title_url(title_url)
        if hit:
            cls._delete_object_from_db(hit)
            return True
        return False

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
