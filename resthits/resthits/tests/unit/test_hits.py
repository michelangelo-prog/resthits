from unittest import TestCase

from marshmallow import ValidationError
from slugify import slugify

from resthits.domain.models.hits import Hit
from resthits.tests.factories import HitDictFactory


class TestHit(TestCase):
    def test_creation_hit_object(self):
        hit_data = HitDictFactory(title="Test test test", artist_id=9)
        hit = Hit(**hit_data)

        self.assertEqual(hit_data["title"], hit.title)
        self.assertEqual(hit_data["title_url"], hit.title_url)
        self.assertEqual(hit_data["artist_id"], hit.artist_id)

    def test_set_up_title_url_as_slugify_title_when_title_url_is_not_given(self):
        hit_data = HitDictFactory()
        hit_data.pop("title_url")
        hit = Hit(**hit_data)

        title_url = slugify(hit_data["title"])

        self.assertEqual(title_url, hit.title_url)

    def test_raise_validation_error_when_try_to_assign_none_to_title(self):
        hit_data = HitDictFactory(title=None)

        with self.assertRaises(ValidationError) as error:
            Hit(**hit_data)

        self.assertEqual(str(error.exception), "Field 'title' not provided.")

    def test_raise_validation_error_when_try_to_assign_empty_string_to_title(self):
        hit_data = HitDictFactory(title="")

        with self.assertRaises(ValidationError) as error:
            Hit(**hit_data)

        self.assertEqual(str(error.exception), "Field 'title' not provided.")
