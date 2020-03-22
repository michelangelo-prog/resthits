from resthits.tests.component.mixins import ArtistMixin, BaseTestCase


class TestHitBlueprint(ArtistMixin, BaseTestCase):
    def test_get_twenty_hits_sorted_by_date(self):
        hit_list = self._given_hits(number=40)

        response = self.get_twenty_best_hits()
        response_json = response.json

        self.assertEqual(200, response.status_code)
        self.assertEqual(20, len(response_json))
        for hit_json, hit_db in zip(response_json, hit_list[-1:-20:-1]):
            self.assertEqual(hit_db.id, hit_json["id"])
            self.assertEqual(hit_db.title, hit_json["title"])
            self.assertEqual(hit_db.title_url, hit_json["titleUrl"])

    def _given_hits(self, number):
        hit_list = []
        for i in range(40):
            artist = self._create_artist_without_hits_in_db()
            hit = self._add_hit_to_artist(artist)
            hit_list.append(hit)
        return hit_list

    def test_return_204_when_get_twenty_hits_and_no_hits_in_db(self):
        response = self.get_twenty_best_hits()

        self.assertEqual(204, response.status_code)

    def test_get_hit_details(self):
        hit_list = self._given_hits(number=2)
        hit = hit_list[0]

        response = self.get_hit_details(title_url=hit.title_url)

        self.assertEqual(200, response.status_code)
        expected_json = self._get_hit_detail_expected_json(hit)
        self.assertEqual(expected_json, response.json)

    def _get_hit_detail_expected_json(self, hit):
        return {
            "id": hit.id,
            "title": hit.title,
            "titleUrl": hit.title_url,
            "createdAt": hit.created_at.strftime("%Y-%m-%dT%H:%M:%S%Z"),
            "artist": {
                "id": hit.artist_id,
                "firstName": hit.artist.first_name,
                "lastName": hit.artist.last_name,
            },
        }

    def test_get_404_when_get_hit_detail_and_hit_with_given_title_url_not_exists(self):
        self._given_hits(number=2)
        response = self.get_hit_details(title_url="test-test-test")
        self.assertEqual(404, response.status_code)
