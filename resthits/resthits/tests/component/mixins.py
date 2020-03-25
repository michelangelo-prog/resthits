from flask_testing import TestCase

from resthits.app.rest import APP_SETTINGS, create_app, db
from resthits.domain.models.artists import Artist
from resthits.domain.models.hits import Hit
from resthits.tests.factories import ArtistDictFactory, HitDictFactory


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config.from_object(APP_SETTINGS["Test"])
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()
        self.db = db

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class DbMixin:
    def _add_object_to_db(self, object):
        db.session.add(object)
        db.session.commit()


class ArtistMixin(DbMixin):
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

    def _get_all_artists_from_db(self):
        return Artist.query.all()

    def _create_artist_without_hits_in_db(self):
        artist_data = ArtistDictFactory()
        artist = Artist(**artist_data)
        self._add_object_to_db(artist)
        self.assertEqual(0, len(artist.hits))
        return artist

    def _create_artist_hits(self, artist, number_of_hits):
        list = []
        for i in range(number_of_hits):
            hit = self._add_hit_to_artist(artist)
            list.append(hit)
        return list

    def _add_hit_to_artist(self, artist):
        data = HitDictFactory(artist_id=artist.id)
        hit = Hit(**data)
        self._add_object_to_db(hit)
        return hit


class HitMixin:
    def get_all_hits_from_db(self):
        return Hit.query.all()
