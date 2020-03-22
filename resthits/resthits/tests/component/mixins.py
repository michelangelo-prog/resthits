from flask_testing import TestCase

from resthits.app.rest import APP_SETTINGS, create_app, db
from resthits.domain.models.artists import Artist


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config.from_object(APP_SETTINGS["Test"])
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class DbMixin:
    def _add_object_to_db(self, object):
        db.session.add(object)
        db.session.commit()


class ArtistMixin:
    def _get_all_artists_from_db(self):
        return Artist.query.all()
