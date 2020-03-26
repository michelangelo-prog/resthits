from resthits.domain.utils import SampleDataFactory
from resthits.tests.component.mixins import BaseTestCase, DbMixin


class TestSampleDataFactory(DbMixin, BaseTestCase):
    def test_create_sample_data(self):
        self.__number_of_hits_in_db_is_equal(0)

        expected_hits_generated = 10
        factory = SampleDataFactory(database=self.db)
        factory.add_sample_hits_to_db(expected_hits_generated)

        self.__number_of_hits_in_db_is_equal(expected_hits_generated)

    def __number_of_hits_in_db_is_equal(self, number):
        hits = self._get_all_hits_from_db()
        self.assertEqual(number, len(hits))
