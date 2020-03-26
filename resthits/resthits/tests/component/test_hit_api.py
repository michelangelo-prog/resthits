from resthits.tests.component.mixins import BaseTestCase, DbMixin, HitMixin
from resthits.tests.factories import HitFactory


class TestHitBlueprint(HitMixin, DbMixin, BaseTestCase):
    def setUp(self):
        super().setUp()
        self.__given_thirty_hits_in_db()

    def __given_thirty_hits_in_db(self):
        self.hits = self._create_hits_in_db(number=30)

    def _create_hits_in_db(self, number):
        return [self._create_hit() for i in range(number)]

    def _create_hit(self):
        hit = HitFactory()
        self._add_object_to_db(hit)
        return hit

    def test_get_twenty_hits_sorted_by_date(self):
        response = self.__when_get_twenty_best_hits()
        self.__then_last_twenty_hits_in_response(response)

    def __when_get_twenty_best_hits(self):
        return self.get_twenty_best_hits()

    def __then_last_twenty_hits_in_response(self, response):
        response_json = response.json
        self.assertEqual(200, response.status_code)
        self.assertEqual(20, len(response_json))
        last_twenty_hits = self.hits[-1:-20:-1]
        for hit_json, hit_db in zip(response_json, last_twenty_hits):
            self.assertEqual(hit_db.id, hit_json["id"])
            self.assertEqual(hit_db.title, hit_json["title"])
            self.assertEqual(hit_db.title_url, hit_json["titleUrl"])

    def test_return_204_when_get_twenty_hits_and_no_hits_in_db(self):
        self._remove_hits_from_db()

        response = self.__when_get_twenty_best_hits()
        self.__then_response_is_204(response)

    def __remove_all_hits_from_db(self):
        self._remove_hits_from_db()

    def __then_response_is_204(self, response):
        self.assertEqual(204, response.status_code)

    def _remove_hits_from_db(self):
        for hit in self.hits:
            self._delete_object_from_db(hit)
        self.assertEqual(0, len(self._get_all_hits_from_db()))

    def test_get_hit_details(self):
        hit = self.hits[0]
        response = self.__when_get_hit_details(hit.title_url)
        self.__then_response_contains_hit_details(response, hit)

    def __when_get_hit_details(self, title_url):
        response = self.get_hit_details(title_url=title_url)
        return response

    def __then_response_contains_hit_details(self, response, hit):
        self.assertEqual(200, response.status_code)
        expected_json = self._create_expected_json_for_hit_details(hit)
        self.assertEqual(expected_json, response.json)

    def _create_expected_json_for_hit_details(self, hit):
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
        response = self.__when_get_hit_details(title_url="test-test-test")
        self.__then_response_is_404(response)

    def __then_response_is_404(self, response):
        expected_json = {"error": "Not found"}
        self.assertEqual(404, response.status_code)
        self.assertEqual(expected_json, response.json)

    def test_add_hit(self):
        hit = self.hits[0]
        artist = hit.artist
        data = {"artistId": hit.artist_id, "title": "test title"}

        response = self.__when_add_hit(data)
        self.__then_response_is_201(response)
        self.__then_hit_is_added_to_artist(artist, data)

    def __when_add_hit(self, json):
        response = self.create_hit(json=json)
        return response

    def __then_hit_is_added_to_artist(self, artist, data_sent):
        self.assertEqual(len(self.hits) + 1, len(self._get_all_hits_from_db()))
        self.assertEqual(2, len(artist.hits))
        self.assertEqual(data_sent["title"], artist.hits[1].title)

    def __then_response_is_201(self, response):
        self.assertEqual(201, response.status_code)

    def test_return_400_when_create_hit_without_artistId(self):
        data = {"title": "test title"}

        response = self.__when_add_hit(data)
        self.__then_response_is_400(response)

    def __then_response_is_400(self, response):
        expected_json = {"error": "Bad Request"}
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected_json, response.json)

    def test_return_400_when_create_hit_without_title(self):
        hit = self.hits[0]
        artist = hit.artist
        data = {"artistId": artist.id}

        response = self.__when_add_hit(data)
        self.__then_response_is_400(response)

    def test_return_400_when_create_hit_with_title_as_none(self):
        hit = self.hits[0]
        artist = hit.artist
        data = {"artistId": artist.id, "title": None}

        response = self.__when_add_hit(data)
        self.__then_response_is_400(response)

    def test_update_hit(self):
        hit = self.hits[0]
        artist_1 = hit.artist
        artist_2 = self.hits[1].artist
        data = {"artistId": artist_2.id, "title": "Test", "titleUrl": "test-test"}

        response = self.__when_update_hit(hit.title_url, data)
        self.__then_response_is_204(response)
        self.__then_hit_has_been_updated_and_assigned_to_another_artist(
            hit, artist_1, artist_2, data
        )

    def __when_update_hit(self, title_url, data):
        response = self.update_hit(title_url=title_url, json=data)
        return response

    def __then_hit_has_been_updated_and_assigned_to_another_artist(
        self, updated_hit, artist_1, artist_2, data
    ):
        self.assertEqual(0, len(artist_1.hits))
        self.assertEqual(2, len(artist_2.hits))
        self.assertEqual(data["artistId"], updated_hit.artist_id)
        self.assertEqual(data["title"], updated_hit.title)
        self.assertEqual(data["titleUrl"], updated_hit.title_url)

    def test_return_400_when_try_update_hit_which_does_not_exist(self):
        hit = self.hits[0]
        artist_1 = hit.artist
        data = {"artistId": artist_1.id, "title": "Test", "titleUrl": "test-test"}

        response = self.update_hit(title_url="TEST", json=data)

        self.__then_response_is_400(response)

    def test_delete_hit(self):
        hit = self.hits[0]
        artist = hit.artist

        response = self.__when_delete_hit(hit.title_url)

        self.__then_response_is_204(response)
        self.__then_artist_has_no_hit(artist)

    def __when_delete_hit(self, title_url):
        response = self.delete_hit(title_url=title_url)
        return response

    def __then_artist_has_no_hit(self, artist):
        self.assertEqual(0, len(artist.hits))

    def test_return_400_when_try_to_delete_not_existing_hit(self):
        response = self.__when_delete_hit(title_url="TEST")
        self.__then_response_is_400(response)
