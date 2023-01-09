from domains.complements.model import Complement
import random

from repository.abstractions import AbstractJsonRepo, AbstractComplementRepo


class ComplementsJsonRepo(AbstractJsonRepo, AbstractComplementRepo):

    def get_random_complement(self) -> Complement:
        complement = random.choice(self.base.get('complements', []))
        return Converter.complement_row_to_object(complement)


class Converter:
    @classmethod
    def complement_row_to_object(cls, row: dict) -> Complement:
        return Complement(
            complement_id=row['id'],
            text=row['text'],
            pic_url=row['pic']
        )
