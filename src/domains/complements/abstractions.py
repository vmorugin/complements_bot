import abc

from domains.complements.model import Complement


class ComplementRepoABC(abc.ABC):

    @abc.abstractmethod
    def get_random_complement(self) -> Complement:
        ...
