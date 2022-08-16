"""
    Author: Edmond Ghislain MAKOLLE

"""
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Tuple

from core.business_logic.setting import Setting


def _aws_folder_exist() -> Tuple[bool, str]:
    """Return the statut of the folder, either exist or not, and the path of
    the folder either exist.

    :return: tuple[bool, str]
    """
    home = Path.home()
    directory_aws = os.path.join(str(home), ".aws/")
    aws_folder = os.path.isdir(directory_aws)
    return aws_folder, directory_aws


def _check_existence(path: str, file: str) -> Tuple[bool, str]:
    """Checks if the file name entered in parameter exists in the given
    directory.

    :param path: (String) path of the directory.
    :param file: (String) name of the file.
    :return: tuple
    """
    file_path = os.path.join(path, file)
    aws_file_exist = Path(file_path).is_file()
    return aws_file_exist, file_path


def _aws_config_file_exist() -> Tuple[bool, str]:
    """Return the statut of the config file, either exist or not, and the path
    of the file either exist.

    :return: tuple[bool, str]
    """
    _, _path = _aws_folder_exist()
    return _check_existence(_path, "config")


def _aws_credentials_file_exist() -> Tuple[bool, str]:
    """Return the statut of the credentials file, either exist or not, and the
    path of the file either exist.

    :return: tuple[bool, str]
    """
    _, _path = _aws_folder_exist()
    return _check_existence(_path, "credentials")


@dataclass()
class AwsSetting(Setting):
    """Class for configuration of local AWS setting."""

    __region: Optional[str] = None
    __access_key_id: Optional[str] = None
    __secret_access_key: Optional[str] = None
    __output: Optional[str] = None

    @property
    def region(self) -> Optional[str]:
        """Getter current region configuration.

        :return: str | None
        """
        logging.info("Getting AWS Region")
        status, _path = _aws_config_file_exist()
        if status:
            with open(_path, "r") as file:
                for line in file.readlines():
                    if "region" in line:
                        self.__region = line.split("=")[1].rstrip("\n")
                        return self.__region

        return None

    def get_credentials(self) -> Optional[Tuple]:
        """Getter account credentials.

        :return: tuple(str, str) | None
        """
        logging.info("Getting AWS Credentials")

        status, _path = _aws_credentials_file_exist()
        if status:
            with open(_path, "r") as file:
                for line in file.readlines():
                    if "aws_access_key_id" in line:
                        self.__access_key_id = line.split("=")[1].rstrip("\n")

                    if "aws_secret_access_key" in line:
                        self.__secret_access_key = line.split("=")[1].rstrip(
                            "\n"
                        )
                return self.__access_key_id, self.__secret_access_key

        return None

    def set_credentials(self, *args) -> None:
        """Configure the credentials file of the AWS directory, if the
        directory does not exist, it creates it.

        :param access_key: (String) Represents the AWS Access Key id.
        :param secret_access_key: (String) Represents the AWS Secret Access
         Key.
        :return: None
        """
        logging.info("Setting AWS Credentials")

        status, _path = _aws_folder_exist()
        _, file_credentials_path = _aws_credentials_file_exist()

        if not status:
            os.mkdir(_path)  # aws folder created

        with open(file_credentials_path, "w") as file:
            file.write("[default]\n")
            file.write(f"aws_access_key_id={args[0]}\n")
            file.write(f"aws_secret_access_key={args[0]}\n")

    @property
    def config(self):
        """

        :return:
        """
        logging.info("Getting AWS Configuration")

        status, _path = _aws_config_file_exist()
        if status:
            with open(_path, "r") as file:
                for line in file.readlines():
                    if "output" in line:
                        self.__output = line.split("=")[1].rstrip("\n")

                return self.region, self.__output

        return None

    @config.setter
    def config(self, tupl: tuple) -> None:
        """Configure the config file of the AWS directory, if the directory
        does not exist, it creates it.

        :param tupl: (Tuple) represent data to set, the AWS region and/or
        the AWS CLI output format. By default, the output it's set at json.
        :return: None
        """
        logging.info("Setting AWS Configuration")

        region = None
        output = "json"

        if len(tupl) > 1:
            region = tupl[0]
            output = tupl[1]
        else:
            region = tupl[0]

        statut, _path = _aws_folder_exist()
        _, file_config_path = _aws_config_file_exist()

        if not statut:
            os.mkdir(_path)  # aws folder created

        with open(file_config_path, "w") as file:
            file.write("[default]\n")
            file.write(f"region={region}\n")
            file.write(f"output={output}\n")

    def authentication(self, access_key: str, secret_access_key: str) -> Any:
        pass
