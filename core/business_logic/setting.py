"""
    Author: Edmond Ghislain MAKOLLE

"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class Setting(ABC):
    @abstractmethod
    def set_credentials(self, access_key: str, secret_access_key: str) -> None:
        pass

    @abstractmethod
    def get_credentials(self) -> Optional[tuple]:
        pass

    @abstractmethod
    def region(self) -> Optional[str]:
        pass

    @abstractmethod
    def authentication(self, access_key: str, secret_access_key: str) -> Any:
        pass
