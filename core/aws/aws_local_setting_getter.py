"""
    Author: Edmond Ghislain MAKOLLE

"""
from dataclasses import dataclass

from core.aws.aws_setting_checker import AwsSettingChecker


@dataclass()
class AwsLocalSettingGetter:
    """Class for retrieve local setting information."""

    checker = AwsSettingChecker()

    def get_region(self):
        """Get the current region configuration.

        :return: str | None
        """
        status, _path = self.checker.aws_config_file_exist()
        if status:
            with open(_path, "r") as file:
                for line in file.readlines():
                    if "region" in line:
                        return line.split("=")[1].rstrip("\n")

        return None

    def get_output(self):
        """Get the current output configuration.

        :return: str | None
        """
        status, _path = self.checker.aws_config_file_exist()
        if status:
            with open(_path, "r") as file:
                for line in file.readlines():
                    if "output" in line:
                        return line.split("=")[1].rstrip("\n")

        return None

    def get_aws_access_key_id(self):
        """Get the current AWS Access Key id.

        :return: str | None
        """
        status, _path = self.checker.aws_credentials_file_exist()
        if status:
            with open(_path, "r") as file:
                for line in file.readlines():
                    if "aws_access_key_id" in line:
                        return line.split("=")[1].rstrip("\n")

        return None

    def get_aws_secret_access_key(self):
        """Get the current AWS Secret Access Key.

        :return: str | None
        """
        status, _path = self.checker.aws_credentials_file_exist()
        if status:
            with open(_path, "r") as file:
                for line in file.readlines():
                    if "aws_secret_access_key" in line:
                        return line.split("=")[1].rstrip("\n")

        return None
