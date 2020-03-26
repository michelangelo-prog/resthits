from resthits.tests.component.mixins import BaseTestCase, DbMixin
from resthits.tests.factories import HitFactory


class TestHits(DbMixin, BaseTestCase):
    def test_create_hit_object_in_db(self):
        data = {"title": "test test", "title_url": "test-test"}
        hit = HitFactory(**data)

        self._add_object_to_db(hit)
        hits_from_db = self._get_all_hits_from_db()

        self.assertEqual(1, len(hits_from_db))
        hit_from_db = hits_from_db[0]
        self.assertEqual(data["title"], hit_from_db.title)
        self.assertEqual(data["title_url"], hit_from_db.title_url)
