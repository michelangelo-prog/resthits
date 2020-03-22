from factory import DictFactory, Sequence


class ArtistDictFactory(DictFactory):

    first_name = Sequence(lambda n: f"first_name_{n}")
    last_name = Sequence(lambda n: f"last_name_{n}")
