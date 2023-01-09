import typing as t


class Complement:
    def __init__(self, complement_id: int, text: str, pic_url: t.Optional[str]):
        self._complement_id = complement_id
        self._text = text
        self._pic_url = pic_url

    @property
    def complement_id(self):
        return self._complement_id

    @property
    def text(self):
        return self._text

    @property
    def pic_url(self):
        return self._pic_url
