from resthits.domain.models.artists import Artist
from resthits.tests.component.mixins import ArtistMixin, BaseTestCase
from resthits.tests.factories import ArtistDictFactory


class TestArtist(ArtistMixin, BaseTestCase):
    def test_creation_artist_object_in_db(self):
        artist_data = ArtistDictFactory(first_name="Test", last_name="TestTest")
        artist = Artist(**artist_data)
        self._add_object_to_db(artist)
        artists_from_db = self._get_all_artists_from_db()

        self.assertEqual(1, len(artists_from_db))
        artist_from_db = artists_from_db[0]
        self.assertEqual(artist_data["first_name"], artist_from_db.first_name)
        self.assertEqual(artist_data["last_name"], artist_from_db.last_name)
