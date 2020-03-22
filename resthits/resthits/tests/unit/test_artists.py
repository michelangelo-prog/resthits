from unittest import TestCase

from marshmallow import ValidationError

from resthits.domain.models.artists import Artist
from resthits.tests.factories import ArtistDictFactory


class TestArtist(TestCase):
    def test_creation_artist_object(self):
        artist_data = ArtistDictFactory(first_name="Test", last_name="TestTest")
        artist = Artist(**artist_data)

        self.assertEqual(artist_data["first_name"], artist.first_name)
        self.assertEqual(artist_data["last_name"], artist.last_name)

    def test_raise_validation_error_when_try_to_assign_none_to_first_name(self):
        artist_data = ArtistDictFactory(first_name=None)

        with self.assertRaises(ValidationError) as error:
            Artist(**artist_data)

        self.assertEqual(str(error.exception), "Field 'first_name' not provided.")

    def test_raise_validation_error_when_try_to_assign_empty_string_to_first_name(self):
        artist_data = ArtistDictFactory(first_name="")

        with self.assertRaises(ValidationError) as error:
            Artist(**artist_data)

        self.assertEqual(str(error.exception), "Field 'first_name' not provided.")

    def test_raise_validation_error_when_try_to_assign_none_to_last_name(self):
        artist_data = ArtistDictFactory(last_name=None)

        with self.assertRaises(ValidationError) as error:
            Artist(**artist_data)

        self.assertEqual(str(error.exception), "Field 'last_name' not provided.")

    def test_raise_validation_error_when_try_to_assign_empty_string_to_last_name(self):
        artist_data = ArtistDictFactory(last_name="")

        with self.assertRaises(ValidationError) as error:
            Artist(**artist_data)

        self.assertEqual(str(error.exception), "Field 'last_name' not provided.")
