from resthits.domain.utils import SampleDataFactory
from resthits.tests.component.mixins import BaseTestCase, HitMixin


class TestSampleDataFactory(HitMixin, BaseTestCase):
    def test_create_sample_data(self):
        number_of_hits = 10
        factory = SampleDataFactory(database=self.db)
        factory.add_sample_hits_to_db(number_of_hits)

        hits = self.get_all_hits_from_db()

        self.assertEqual(number_of_hits, len(hits))
