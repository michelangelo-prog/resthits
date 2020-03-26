from resthits.tests.component.mixins import BaseTestCase, DbMixin
from resthits.tests.factories import ArtistFactory


class TestArtist(DbMixin, BaseTestCase):
    def test_creation_artist_object_in_db(self):
        data = {"first_name": "Test", "last_name": "TestTest"}
        artist = ArtistFactory(**data)
        self._add_object_to_db(artist)
        artists_from_db = self._get_all_artists_from_db()

        self.assertEqual(1, len(artists_from_db))
        artist_from_db = artists_from_db[0]
        self.assertEqual(data["first_name"], artist_from_db.first_name)
        self.assertEqual(data["last_name"], artist_from_db.last_name)
