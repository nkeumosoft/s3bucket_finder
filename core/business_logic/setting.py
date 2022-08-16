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
<<<<<<< HEAD
    def get_credentials(self) -> Optional[Any]:
=======
    def get_credentials(self) -> Optional[dict]:
>>>>>>> b0d3386 (Change the tuple to dict)
        pass


class Setting(GlobalSettings):
    @abstractmethod
    def region(self) -> Optional[str]:
        pass

    @abstractmethod
    def authentication(self, access_key: str, secret_access_key: str) -> Any:
        pass
