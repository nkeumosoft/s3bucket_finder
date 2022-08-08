"""
    Author: Edmond Ghislain MAKOLLE

"""
import logging
import os
from dataclasses import dataclass
from typing import Any, Optional

from core.business_logic.setting import Setting


@dataclass()
class DigitalOceanSetting(Setting):
    """Class for configuration of local Digital Ocean Setting."""

    __region: str
    __access_key: Optional[str] = None
    __secret_key: Optional[str] = None

    @property
    def region(self) -> str:
        """Getting the region.

        :return: str
        """
        logging.info("Getting Digital Ocean Region")

        return self.__region

    @region.setter
    def region(self, region: str) -> None:
        """Puts the region.

        :param region: (String) region to put.
        :return: None
        """
        logging.info("Setting Digital Ocean Region")

        self.__region = region

    def set_credentials(self, access_key: str, secret_access_key: str) -> None:
        """Function that puts access key and secret access in environment
        variables.

        :param access_key: (String) represent a Digital Ocean access key
        :param secret_access_key: (String) represent a Digital Ocean secret
         access
        :return: None
        """
        logging.info("Setting Digital Ocean Credentials")

        os.environ["SPACES_KEY"] = access_key
        os.environ["SPACES_SECRET"] = secret_access_key

    def get_credentials(self) -> Optional[tuple]:
        """Function that retrieves access key and secret access from
        environment variables.

        :return: tuple(str, str) | None
        """
        logging.info("Getting Digital Ocean Credentials")

        self.__access_key = os.getenv("SPACES_KEY")
        self.__secret_key = os.getenv("SPACES_KEY")

        return self.__access_key, self.__secret_key

    def authentication(self, access_key: str, secret_access_key: str) -> Any:
        pass
