from resthits.tests.component.mixins import ArtistMixin, BaseTestCase


class TestHitBlueprint(ArtistMixin, BaseTestCase):
    def test_get_twenty_hits_sorted_by_date(self):
        artists = self._given_artist_with_hit(number=40)
        last_twenty_hits = [artist.hits[0] for artist in artists[-1:-20:-1]]

        response = self.get_twenty_best_hits()
        response_json = response.json

        self.assertEqual(200, response.status_code)
        self.assertEqual(20, len(response_json))
        for hit_json, hit_db in zip(response_json, last_twenty_hits):
            self.assertEqual(hit_db.id, hit_json["id"])
            self.assertEqual(hit_db.title, hit_json["title"])
            self.assertEqual(hit_db.title_url, hit_json["titleUrl"])

    def _given_artist_with_hit(self, number):
        artist_list = []
        for i in range(40):
            artist = self._create_artist_without_hits_in_db()
            self._add_hit_to_artist(artist)
            artist_list.append(artist)
        return artist_list

    def test_return_204_when_get_twenty_hits_and_no_hits_in_db(self):
        response = self.get_twenty_best_hits()

        self.assertEqual(204, response.status_code)

    def test_get_hit_details(self):
        artists = self._given_artist_with_hit(number=2)
        hit = artists[0].hits[0]

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
        self._given_artist_with_hit(number=2)
        response = self.get_hit_details(title_url="test-test-test")
        self.assertEqual(404, response.status_code)

    def test_add_hit_using_post_method(self):
        artist = self._create_artist_without_hits_in_db()
        json = {"artistId": artist.id, "title": "test title"}

        response = self.create_hit(json=json)

        self.assertEqual(201, response.status_code)
        self.assertEqual(1, len(artist.hits))
        self.assertEqual(json["title"], artist.hits[0].title)

    def test_return_400_when_create_hit_without_artistId(self):
        json = {"title": "test title"}

        response = self.create_hit(json=json)

        self.assertEqual(400, response.status_code)

    def test_return_400_when_create_hit_without_title(self):
        artist = self._create_artist_without_hits_in_db()
        json = {"artistId": artist.id}

        response = self.create_hit(json=json)

        self.assertEqual(400, response.status_code)

    def test_return_400_when_create_hit_with_title_as_none(self):
        artist = self._create_artist_without_hits_in_db()
        json = {"artistId": artist.id, "title": None}

        response = self.create_hit(json=json)

        self.assertEqual(400, response.status_code)

    def test_update_hit(self):
        artists = self._given_artist_with_hit(number=2)

        hit = artists[0].hits[0]
        data = {"artistId": artists[1].id, "title": "Test", "titleUrl": "test-test"}

        response = self.update_hit(title_url=hit.title_url, json=data)

        self.assertEqual(204, response.status_code)
        self.assertEqual(0, len(artists[0].hits))
        self.assertEqual(2, len(artists[1].hits))
        self.assertEqual(data["artistId"], hit.artist_id)
        self.assertEqual(data["title"], hit.title)
        self.assertEqual(data["titleUrl"], hit.title_url)

    def test_return_400_when_try_update_hit_which_does_not_exist(self):
        artists = self._given_artist_with_hit(number=2)
        data = {"artistId": artists[1].id, "title": "Test", "titleUrl": "test-test"}

        response = self.update_hit(title_url="TEST", json=data)

        self.assertEqual(400, response.status_code)

    def test_delete_hit(self):
        artists = self._given_artist_with_hit(number=2)
        hit = artists[0].hits[0]

        response = self.delete_hit(title_url=hit.title_url)

        self.assertEqual(204, response.status_code)
        self.assertEqual(0, len(artists[0].hits))

    def test_return_400_when_try_to_delete_not_existing_hit(self):
        self._given_artist_with_hit(number=2)
        response = self.delete_hit(title_url="TEST")
        self.assertEqual(400, response.status_code)
