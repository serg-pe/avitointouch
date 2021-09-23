from typing import Tuple
from abc import  ABC, abstractmethod

import requests

from models.models import Advertisement


class Scraper(ABC):
    """Scraper interface"""

    @abstractmethod
    def scrap_pages_quantity(self, page_content) -> int:
        pass

    @abstractmethod
    def scrap_ads(self, page_content: str) -> Tuple[Advertisement]:
        pass
