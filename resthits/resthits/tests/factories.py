from factory import DictFactory, Factory, LazyAttribute, Sequence, SubFactory
from factory.fuzzy import FuzzyInteger
from slugify import slugify

from resthits.domain.models.artists import Artist
from resthits.domain.models.hits import Hit


class ArtistDictFactory(DictFactory):

    first_name = Sequence(lambda n: f"first_name_{n}")
    last_name = Sequence(lambda n: f"last_name_{n}")


class HitDictFactory(DictFactory):
    title = Sequence(lambda n: f"Hit title{n}")
    title_url = Sequence(lambda n: f"hit-title{n}")
    artist_id = FuzzyInteger(0, 5)


class ArtistFactory(Factory):
    class Meta:
        model = Artist

    first_name = Sequence(lambda n: f"first_name_{n}")
    last_name = Sequence(lambda n: f"last_name_{n}")


class HitFactory(Factory):
    class Meta:
        model = Hit

    title = Sequence(lambda n: f"Hit title{n}")
    title_url = LazyAttribute(lambda n: slugify(n.title))
    artist = SubFactory(ArtistFactory)
