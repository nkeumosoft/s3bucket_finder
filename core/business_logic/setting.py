"""
    Author: Edmond Ghislain MAKOLLE

"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class GlobalSettings(ABC):
    @abstractmethod
    def set_credentials(self, *args) -> None:
        pass

    @abstractmethod
    def get_credentials(self) -> Optional[tuple]:
        pass


class Setting(GlobalSettings):
    @abstractmethod
    def region(self) -> Optional[str]:
        pass

    @abstractmethod
    def authentication(self, access_key: str, secret_access_key: str) -> Any:
        pass
