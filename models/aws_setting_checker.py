"""
    Author: Edmond Ghislain MAKOLLE

"""
import os
from pathlib import Path


class AwsSettingChecker:

    aws_folder = False
    aws_config_file = False
    aws_credentials_file = False

    def aws_folder_exist(self):
        home = Path.home()
        directory_aws = os.path.join(str(home), '.aws/')
        self.aws_folder = os.path.isdir(directory_aws)
        return self.aws_folder, directory_aws

    def aws_config_file_exist(self):
        home = Path.home()
        directory_aws = os.path.join(str(home), '.aws/')
        file_config_path = os.path.join(directory_aws, 'config')
        self.aws_config_file = Path(file_config_path).is_file()
        return self.aws_config_file, file_config_path

    def aws_credentials_file_exist(self):
        home = Path.home()
        directory_aws = os.path.join(str(home), '.aws/')
        file_cred_path = os.path.join(directory_aws, 'credentials')
        self.aws_credentials_file = Path(file_cred_path).is_file()
        return self.aws_credentials_file, file_cred_path
