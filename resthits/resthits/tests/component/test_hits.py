from resthits.tests.component.mixins import ArtistMixin, BaseTestCase


class TestHits(ArtistMixin, BaseTestCase):
    def test_create_hit_object_in_db(self):
        number_of_hits = 2
        artist = self._create_artist_without_hits_in_db()
        artist_hits = self._create_artist_hits(artist, number_of_hits)

        self.assertEqual(number_of_hits, len(artist.hits))
        for hit in artist_hits:
            self.assertIn(hit, artist.hits)
