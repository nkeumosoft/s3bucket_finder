"""
    Author: Edmond Ghislain MAKOLLE

"""
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

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

    __region: str
    __access_key_id: str
    __secret_access_key: str
    __output: str

    @property
    def region(self) -> Optional[str]:
        """Getter current region configuration.

        :return: str | None
        """
        logging.info("Getting Region")
        status, _path = _aws_config_file_exist()
        if status:
            with open(_path, "r") as file:
                for line in file.readlines():
                    if "region" in line:
                        self.__region = line.split("=")[1].rstrip("\n")
                        return self.__region

        return None

    @property
    def output(self) -> Optional[str]:
        """Getter current output configuration.

        :return: str | None
        """
        logging.info("Getting Output")
        status, _path = _aws_config_file_exist()
        if status:
            with open(_path, "r") as file:
                for line in file.readlines():
                    if "output" in line:
                        return line.split("=")[1].rstrip("\n")

        return None

    @property
    def get_credentials(self) -> Optional[Tuple[str, str]]:
        """Getter account credentials.

        :return:
        """
        logging.info("Getting Credentials")

        status, _path = _aws_credentials_file_exist()
        if status:
            with open(_path, "r") as file:
                for line in file.readlines():
                    if "aws_access_key_id" in line:
                        self.__access_key_id = line.split("=")[1].rstrip("\n")

                    if "aws_secret_access_key" in line:
                        self.__secret_access_key = line.split("=")[1].rstrip("\n")
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
        logging.info("Setting Credentials")

        self.__secret_access_key = args[0]
        self.__access_key_id = args[1]

        status, _path = _aws_folder_exist()
        _, file_credentials_path = _aws_credentials_file_exist()

        if not status:
            os.mkdir(_path)  # aws folder created

        with open(file_credentials_path, "w") as file:
            file.write("[default]\n")
            file.write(f"aws_access_key_id={self.__access_key_id}\n")
            file.write(f"aws_secret_access_key={self.__secret_access_key}\n")

    def setup_config(self, region: str, output: str = "json") -> None:
        """Configure the config file of the AWS directory, if the directory
        does not exist, it creates it.

        :param region: (String) Represents the AWS region.
        :param output: (String) Represents the AWS CLI output
                        format. By default, it's set at json.
        :return: None
        """
        logging.info("Getting Configuration")

        self.__region = region
        self.__output = output

        statut, _path = _aws_folder_exist()
        _, file_config_path = _aws_config_file_exist()

        if not statut:
            os.mkdir(_path)  # aws folder created

        with open(file_config_path, "w") as file:
            file.write("[default]\n")
            file.write(f"region={self.__region}\n")
            file.write(f"output={self.__output}\n")
