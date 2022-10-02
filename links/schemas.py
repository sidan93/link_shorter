from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from utils.utils import URL_REGEX


class Link(BaseModel):
    long_url: Optional[str] = None
    short_url: Optional[str] = None
    visits: Optional[int] = None
    created_at: Optional[datetime] = None

    def prepare_url(self) -> bool:
        if not self.long_url:
            return False

        if not URL_REGEX.match(self.long_url):
            return False

        # добавим http если его нет
        if not self.long_url.startswith('http'):
            self.long_url = 'http://' + self.long_url

        return True
