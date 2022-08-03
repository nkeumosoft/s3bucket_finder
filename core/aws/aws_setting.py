"""
    Author: Edmond Ghislain MAKOLLE

"""

import os

from core.aws.aws_setting_checker import AwsSettingChecker
from interface import setting


class AwsSetting(setting.Setting):
    """Class for configuration of local AWS setting."""

    def __init__(self):
        """Initialization of the AWS Setting Class."""
        self.__region = None
        self.__key_id = None
        self.__key_access = None
        self.__output = None
        self.__checker = AwsSettingChecker()

    @property
    def region(self):
        """Getter region."""
        print("Getting region")
        return self.__region

    @property
    def aws_access_key_id(self):
        """Getter AWS Access Key Id."""
        print("Getting AWS Access Key Id")
        return self.__key_id

    @property
    def aws_secret_access_key(self):
        """Getter AWS Secret Access Key."""
        print("Getting AWS Secret Access Key")
        return self.__key_access

    @property
    def output(self):
        """Getter output."""
        print("Getting Output")
        return self.__output

    def setup_config(self, region: str, output: str = "json") -> None:
        """Configure the config file of the AWS directory, if the directory
        does not exist, it creates it.

        :param region: (String) Represents the AWS region.
        :param output: (String) Represents the AWS CLI output
                        format. By default, it's set at json.
        :return: None
        """
        statut, _path = self.__checker.aws_folder_exist()
        _, file_config_path = self.__checker.aws_config_file_exist()
        if not statut:
            os.mkdir(_path)  # aws folder created
        with open(file_config_path, "w") as file:
            file.write("[default]\n")
            file.write(f"region={region}\n")
            file.write(f"output={output}\n")
        self.__region = region
        self.__output = output

    def setup_credentials(self, the_id: str, the_key: str) -> None:
        """Configure the credentials file of the AWS directory, if the
        directory does not exist, it creates it.

        :param the_id: (String) Represents the AWS Access Key id.
        :param the_key: (String) Represents the AWS Secret Access Key.
        :return: None
        """
        status, _path = self.__checker.aws_folder_exist()
        _, file_credentials_path = self.__checker.aws_credentials_file_exist()
        if not status:
            os.mkdir(_path)  # aws folder created
        with open(file_credentials_path, "w") as file:
            file.write("[default]\n")
            file.write(f"aws_access_key_id={the_id}\n")
            file.write(f"aws_secret_access_key={the_key}\n")
        self.__key_id = the_id
        self.__key_access = the_key
