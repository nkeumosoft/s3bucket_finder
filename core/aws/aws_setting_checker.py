"""
    Author: Edmond Ghislain MAKOLLE

"""
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass()
class AwsSettingChecker:
    """AWS Setting Checker class."""

    aws_folder = False
    aws_config_file = False
    aws_credentials_file = False

    def aws_folder_exist(self):
        """Return the statut of the folder, either exist or not, and the path
        of the folder either exist.

        :return: tuple[bool, str]
        """
        home = Path.home()
        directory_aws = os.path.join(str(home), ".aws/")
        self.aws_folder = os.path.isdir(directory_aws)
        return self.aws_folder, directory_aws

    def aws_config_file_exist(self):
        """Return the statut of the config file, either exist or not, and the
        path of the file either exist.

        :return: tuple[bool, str]
        """
        _, _path = self.aws_folder_exist()
        file_config_path = os.path.join(_path, "config")
        self.aws_config_file = Path(file_config_path).is_file()
        return self.aws_config_file, file_config_path

    def aws_credentials_file_exist(self):
        """Return the statut of the credentials file, either exist or not, and
        the path of the file either exist.

        :return: tuple[bool, str]
        """
        _, _path = self.aws_folder_exist()
        file_cred_path = os.path.join(_path, "credentials")
        self.aws_credentials_file = Path(file_cred_path).is_file()
        return self.aws_credentials_file, file_cred_path
