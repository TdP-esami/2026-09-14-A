from dataclasses import dataclass, field


@dataclass
class Actor:
    NameId: str
    Name: str
    DateOfBirth: object = None
    # lista di dict dei film (con valutazione nell'intervallo selezionato dall'utente) in cui l'attore recita
    Movies: list = field(default_factory=list)

    def __hash__(self):
        return hash(self.NameId)

    def __eq__(self, other):
        if not isinstance(other, Actor):
            return False
        return self.NameId == other.NameId

    def __str__(self):
        return f"{self.Name}"

    def get_movie_ids(self):
        """Ritorna l'insieme degli id dei film in cui l'attore recita."""
        return {movie["movie_id"] for movie in self.Movies}

    def get_num_movies(self):
        return len(self.Movies)
