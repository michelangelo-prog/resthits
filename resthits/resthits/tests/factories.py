from factory import DictFactory, Sequence
from factory.fuzzy import FuzzyInteger


class ArtistDictFactory(DictFactory):

    first_name = Sequence(lambda n: f"first_name_{n}")
    last_name = Sequence(lambda n: f"last_name_{n}")


class HitDictFactory(DictFactory):
    title = Sequence(lambda n: f"Hit title {n}")
    title_url = Sequence(lambda n: f"hit-title-{n}")
    artist_id = FuzzyInteger(0, 5)
