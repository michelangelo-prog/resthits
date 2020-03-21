from resthits.tests.factories import ArtistFactory
from resthits.tests.mixins import ArtistMixin, BaseTestCase, DbMixin


class TestArtist(DbMixin, ArtistMixin, BaseTestCase):
    def test_creation_artist_object(self):
        first_name = "Test"
        last_name = "TestTest"
        artist = ArtistFactory(first_name=first_name, last_name=last_name)
        self._add_object_to_db(artist)
        artists_from_db = self._get_all_artists_from_db()

        self.assertEqual(1, len(artists_from_db))
        artist_from_db = artists_from_db[0]
        self.assertEqual(first_name, artist_from_db.first_name)
        self.assertEqual(last_name, artist_from_db.last_name)
