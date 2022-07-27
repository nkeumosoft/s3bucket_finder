import os
from pathlib import Path


def setup_config(region: str, output="json") -> None:
    """
    Configure the config file of the AWS directory, if the directory does not exist, it creates it.

    :param region: (String) Represents the AWS region.
    :param output: (String) Represents the AWS CLI output format. By default, it's set at json.
    :return: None
    """
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
        os.mkdir(directory_aws)     # aws folder created
        with open(file_config_path, "w") as f:
            f.write("[default]\n")
            f.write(f"region={region}\n")
            f.write(f"output={output}\n")


def setup_credentials(id: str, key: str) -> None:
    """
    Configure the credentials file of the AWS directory, if the directory does not exist, it creates it.

    :param id: (String) Represents the AWS Access Key id.
    :param key: (String) Represents the AWS Secret Access Key
    :return: None
    """
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


def get_region() -> str | None:
    """
    Return the current region of the local config file.
    If the config file don't exist, return None.

    :return: str | None
    """
    home = Path.home()
    directory_aws = os.path.join(str(home), '.aws/')
    is_dir_aws = os.path.isdir(directory_aws)
    file_config_path = os.path.join(directory_aws, 'config')
    config_file_exists = Path(file_config_path).is_file()
    if is_dir_aws and config_file_exists:
        # aws folder exist
        with open(file_config_path, "r") as f:
            for line in f.readlines():
                if "region" in line:
                    return line.split("=")[1].rstrip("\n")
    else:
        print("Your AWS config file don't exist ! Create it !")
    return None
