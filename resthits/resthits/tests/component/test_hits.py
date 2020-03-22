from resthits.domain.models.artists import Artist
from resthits.domain.models.hits import Hit
from resthits.tests.component.mixins import BaseTestCase, DbMixin
from resthits.tests.factories import ArtistDictFactory, HitDictFactory


class TestHits(DbMixin, BaseTestCase):
    def test_create_hit_object_in_db(self):
        number_of_hits = 2
        artist = self._create_artist_without_hits_in_db()
        artist_hits = self._create_artist_hits(artist, number_of_hits)

        self.assertEqual(number_of_hits, len(artist.hits))
        for hit in artist_hits:
            self.assertIn(hit, artist.hits)

    def _create_artist_without_hits_in_db(self):
        artist_data = ArtistDictFactory()
        artist = Artist(**artist_data)
        self._add_object_to_db(artist)
        self.assertEqual(0, len(artist.hits))
        return artist

    def _create_artist_hits(self, artist, number_of_hits):
        list = []
        for i in range(number_of_hits):
            data = HitDictFactory(artist_id=artist.id)
            hit = Hit(**data)
            self._add_object_to_db(hit)
            list.append(hit)
        return list
