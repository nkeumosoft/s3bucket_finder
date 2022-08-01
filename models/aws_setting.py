"""
    Author: Edmond Ghislain MAKOLLE

"""

import os

from interface.setting import Setting
from models.aws_setting_checker import AwsSettingChecker


class AwsSetting(Setting):

    def __init__(self):
        """Initialization of the AWS Setting Class."""
        self.__region = None
        self.__key_id = None
        self.__key_access = None
        self.__output = None
        self.__checker = AwsSettingChecker()

    def get_region(self):
        """
        Get the current region configuration.

        :return: str | None
        """
        return self.__region

    def get_key_id(self):
        """
        Get the current AWS Access Key id.

        :return: str | None
        """
        return self.__key_id

    def get_key_access(self):
        """
        Get the current AWS Secret Access Key.

        :return: str | None
        """
        return self.__key_access

    def get_output(self):
        """
        Get the current output configuration.

        :return: str | None
        """
        return self.__output

    def setup_config(self, region: str, output: str = "json") -> None:
        """
            Configure the config file of the AWS directory, if the
            directory does not exist, it creates it.

            :param region: (String) Represents the AWS region.
            :param output: (String) Represents the AWS CLI output
                            format. By default, it's set at json.
            :return: None
        """
        statut, _path = self.__checker.aws_folder_exist()
        _, file_config_path = self.__checker.aws_config_file_exist()
        if not statut:
            os.mkdir(_path)    # aws folder created
        with open(file_config_path, "w") as f:
            f.write("[default]\n")
            f.write(f"region={region}\n")
            f.write(f"output={output}\n")
        self.__region = region
        self.__output = output

    def setup_credentials(self, id: str, key: str) -> None:
        """
            Configure the credentials file of the AWS directory, if the
            directory does not exist, it creates it.

            :param id: (String) Represents the AWS Access Key id.
            :param key: (String) Represents the AWS Secret Access Key.
            :return: None
        """
        status, _path = self.__checker.aws_folder_exist()
        _, file_credentials_path = self.__checker.aws_credentials_file_exist()
        if not status:
            os.mkdir(_path)    # aws folder created
        with open(file_credentials_path, "w") as f:
            f.write("[default]\n")
            f.write(f"aws_access_key_id={id}\n")
            f.write(f"aws_secret_access_key={key}\n")
        self.__key_id = id
        self.__key_access = key
