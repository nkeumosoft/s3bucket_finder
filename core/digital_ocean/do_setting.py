"""
    Author: Edmond Ghislain MAKOLLE

"""
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Tuple

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

        status, _path = self.__check_digitalocean_credentials_file()

        if not status:
            os.mkdir(_path)

        with open(_path, "w") as file:
            file.write(f"SPACES_KEY={access_key}\n")
            file.write(f"SPACES_SECRET={secret_access_key}\n")

    def get_credentials(self) -> Optional[dict]:
        """Function that retrieves access key and secret access from
        environment variables.

        :return: dict(str: str) | None
        """
        logging.info("Getting Digital Ocean Credentials")

        status, _path = self.__check_digitalocean_credentials_file()

        if status:
            with open(_path, "r") as file:
                for line in file.readlines():
                    if "SPACES_KEY" in line:
                        self.__access_key = line.split("=")[1].rstrip("\n")

                    if "SPACES_SECRET" in line:
                        self.__secret_key = line.split("=")[1].rstrip("\n")

<<<<<<< HEAD
                return {"access_key": self.__access_key,
                        "secret_key": self.__secret_key}
=======
                return {
                    "access_key": self.__access_key,
                    "secret_key": self.__secret_key,
                }
>>>>>>> b0d3386 (Change the tuple to dict)

        return None

    @staticmethod
    def __check_digitalocean_credentials_file() -> Tuple[bool, str]:
        """Checks if the file credentials configuration of digital ocean
        exists.

        :return: Tuple[Boolean, String]
        """
        file_path = os.path.join(str(Path.home()), ".digitalocean")
        digitalocean_file_exist = Path(file_path).is_file()
        return digitalocean_file_exist, file_path

    def authentication(self, access_key: str, secret_access_key: str) -> Any:
        pass
