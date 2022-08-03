"""
    Author: Edmond Ghislain MAKOLLE

"""

from abc import ABC


class Setting(ABC):
    def setup_config(self, region: str, output: str) -> None:
        """Configure a config file.

        :param region: (String)
        :param output: (String)
        :return: None
        """
        pass

    def setup_credentials(self, id: str, key: str) -> None:
        """Configure a credentials file.

        :param id: (String)
        :param key: (String)
        :return: None
        """
        pass
