from resthits.domain.models.hits import Hit
from resthits.tests.component.mixins import BaseTestCase, DbMixin
from resthits.tests.factories import ArtistFactory, HitFactory


class TestHits(DbMixin, BaseTestCase):
    def setUp(self):
        super().setUp()
        self.artist = self._create_artist()

    def _create_artist(self):
        artist = ArtistFactory()
        self._add_object_to_db(artist)
        return artist

    def test_create_hit_object_in_db(self):
        data = {"title": "test test", "title_url": "test-test"}
        hit = HitFactory(**data)

        self._add_object_to_db(hit)
        hits_from_db = self._get_all_hits_from_db()

        self.assertEqual(1, len(hits_from_db))
        hit_from_db = hits_from_db[-1]
        self.assertEqual(data["title"], hit_from_db.title)
        self.assertEqual(data["title_url"], hit_from_db.title_url)

    def test_add_hit_from_json_data_when_title_url_not_exists(self):
        data = {"artistId": self.artist.id, "title": "test test"}
        hit = Hit.add_hit_from_json_data(data)
        self.assertEqual("test-test", hit.title_url)

    def test_add_hit_from_json_data_when_one_title_url_exists(self):
        data = {"artistId": self.artist.id, "title": "test test"}
        hits = [Hit.add_hit_from_json_data(data) for i in range(2)]
        self.assertEqual("test-test-2", hits[1].title_url)

    def test_add_hit_from_json_data_when_two_title_url_exist(self):
        data = {"artistId": self.artist.id, "title": "test test"}
        hits = [Hit.add_hit_from_json_data(data) for i in range(3)]
        self.assertEqual("test-test-3", hits[2].title_url)
