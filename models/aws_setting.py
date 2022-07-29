"""
    Author: Edmond Ghislain MAKOLLE

"""

import os
from pathlib import Path

from interface.setting import Setting


class AwsSetting(Setting):

    def __init__(self):
        """Initialization of the AWS Setting Class."""
        self.__region = None
        self.__key_id = None
        self.__key_access = None
        self.__output = None

    def get_region(self):
        """
        Get the actual region configuration.

        :return: str
        """
        return self.__region

    def get_key_id(self):
        """
        Get the actual AWS Access Key id.

        :return: str
        """
        return self.__key_id

    def get_key_access(self):
        """
        Get the actual AWS Secret Access Key.

        :return: str
        """
        return self.__key_access

    def get_output(self):
        """
        Get the actual output configuration.

        :return: str
        """
        return self.__output

    def __set_region(self, reg):
        """
        Set the region value.

        :param reg: (String) Region to set
        :return: None
        """
        self.__region = reg

    def __set_key_id(self, key):
        """
        Set the key id value.

        :param key: (String) Key id to set
        :return: None
        """
        self.__key_id = key

    def __set_key_access(self, key):
        """
        Set the key access id value.

        :param key: (String) Key access id to set
        :return: None
        """
        self.__key_access = key

    def __set_output(self, out):
        """
        Set the output value.

        :param out: (String) Output to set
        :return: None
        """
        self.__output = out

    def setup_config(self, region: str, output: str = "json") -> None:
        """
            Configure the config file of the AWS directory, if the
            directory does not exist, it creates it.

            :param region: (String) Represents the AWS region.
            :param output: (String) Represents the AWS CLI output
                            format. By default, it's set at json.
            :return: None
        """
        self.__set_region(region)
        self.__set_output(output)

        home = Path.home()
        directory_aws = os.path.join(str(home), '.aws/')
        is_dir_aws = os.path.isdir(directory_aws)
        file_config_path = os.path.join(directory_aws, 'config')
        if is_dir_aws:
            # aws folder exist
            with open(file_config_path, "w") as f:
                f.write("[default]\n")
                f.write(f"region={region}\n")
                f.write(f"output={output}\n")
        else:
            os.mkdir(directory_aws)  # aws folder created
            with open(file_config_path, "w") as f:
                f.write("[default]\n")
                f.write(f"region={region}\n")
                f.write(f"output={output}\n")

    def setup_credentials(self, id: str, key: str) -> None:
        """
            Configure the credentials file of the AWS directory, if the
            directory does not exist, it creates it.

            :param id: (String) Represents the AWS Access Key id.
            :param key: (String) Represents the AWS Secret Access Key.
            :return: None
        """
        self.__set_key_id(id)
        self.__set_key_access(key)

        home = Path.home()
        directory_aws = os.path.join(str(home), '.aws/')
        is_dir_aws = os.path.isdir(directory_aws)
        file_credentials_path = os.path.join(directory_aws, 'credentials')
        if is_dir_aws:
            # aws folder exist
            with open(file_credentials_path, "w") as f:
                f.write("[default]\n")
                f.write(f"aws_access_key_id={id}\n")
                f.write(f"aws_secret_access_key={key}\n")
        else:
            os.mkdir(directory_aws)  # aws folder created
            with open(file_credentials_path, "w") as f:
                f.write("[default]\n")
                f.write(f"aws_access_key_id={id}\n")
                f.write(f"aws_secret_access_key={key}\n")
