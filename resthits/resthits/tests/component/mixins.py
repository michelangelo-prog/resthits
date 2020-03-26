from flask_testing import TestCase

from resthits.app.rest import APP_SETTINGS, create_app, db
from resthits.domain.models.artists import Artist
from resthits.domain.models.hits import Hit


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config.from_object(APP_SETTINGS["Test"])
        return app

    def setUp(self):
        self.db = db
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class DbMixin:
    def _add_object_to_db(self, object):
        db.session.add(object)
        db.session.commit()

    def _delete_object_from_db(self, object):
        db.session.delete(object)
        db.session.commit()

    def _get_all_hits_from_db(self):
        return Hit.query.all()

    def _get_all_artists_from_db(self):
        return Artist.query.all()


class HitMixin:
    def get_twenty_best_hits(self, **kwargs):
        uri = "/api/v1/hits"
        return self.client.get(uri, **kwargs)

    def get_hit_details(self, title_url, **kwargs):
        uri = "/api/v1/hits/{}".format(title_url)
        return self.client.get(uri, **kwargs)

    def create_hit(self, **kwargs):
        uri = "/api/v1/hits"
        return self.client.post(uri, **kwargs)

    def update_hit(self, title_url, **kwargs):
        uri = "/api/v1/hits/{}".format(title_url)
        return self.client.put(uri, **kwargs)

    def delete_hit(self, title_url, **kwargs):
        uri = "/api/v1/hits/{}".format(title_url)
        return self.client.delete(uri, **kwargs)
