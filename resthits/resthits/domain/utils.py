from resthits.tests.factories import HitFactory


class SampleDataFactory:
    def __init__(self, database):
        self.db = database

    def add_sample_hits_to_db(self, number):
        for i in range(number):
            hit = HitFactory()
            self.db.session.add(hit)
        self.db.session.commit()
