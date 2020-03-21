from factory import Factory, Sequence

from resthits.domain.models.artists import Artist


class ArtistFactory(Factory):
    class Meta:
        model = Artist

    first_name = Sequence(lambda n: f"first_name_{n}")
    last_name = Sequence(lambda n: f"last_name_{n}")
