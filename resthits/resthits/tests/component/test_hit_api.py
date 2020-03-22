from resthits.tests.component.mixins import ArtistMixin, BaseTestCase


class TestHitBlueprint(ArtistMixin, BaseTestCase):
    def test_get_twenty_hits_sorted_by_date(self):
        hit_list = self._given_hit_with_artist(number=40)

        response = self.get_twenty_best_hits()
        response_json = response.json

        self.assertEqual(200, response.status_code)
        self.assertEqual(20, len(response_json))
        for hit_json, hit_db in zip(response_json, hit_list[-1:-20:-1]):
            self.assertEqual(hit_db.id, hit_json["id"])
            self.assertEqual(hit_db.title, hit_json["title"])
            self.assertEqual(hit_db.title_url, hit_json["titleUrl"])

    def _given_hit_with_artist(self, number):
        hit_list = []
        for i in range(40):
            artist = self._create_artist_without_hits_in_db()
            hit = self._add_hit_to_artist(artist)
            hit_list.append(hit)
        return hit_list

    def test_return_204_when_get_twenty_hits_and_no_hits_in_db(self):
        response = self.get_twenty_best_hits()

        self.assertEqual(204, response.status_code)
