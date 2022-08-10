"""
    Author: Noutcheu Libert

"""
import logging
import os
import pathlib
import sys

from google.cloud import storage

from s3bucket_finder.core.business_logic.setting import GlobalSettings
from s3bucket_finder.utils.createcsvfile import makefolder


class CloudStorageSetting(GlobalSettings):
    __path_file_key: str

    def __init__(self, path_file_key: str = None):

        self.set_credentials(path_file_key)

    def __exit__(self):
        self.save_path_file_key()

    def set_credentials(self, path_file_key):
        if path_file_key is not None and check_valid_path(path_file_key):
            self.set_path_file_key(path_file_key)

    def get_credentials(self):
        if self.__path_file_key is not None:
            return self.__path_file_key

    def load_credentials_from_file(self) -> None:
        logging.info("loading credential json file")
        _path = ".google"
        folder_path = makefolder(_path)
        os.chdir(folder_path)
        config = os.listdir()[0]

        with open(folder_path + f"/{config}", "r", encoding="utf-8") as file:

            path_file = file.read()

        if path_file:
            self.path_file_key = path_file
        else:
            logging.error("not file credential found")
            sys.exit(1)

    @property
    def path_file_key(self):
        return self.__path_file_key

    @path_file_key.setter
    def path_file_key(self, path_file_key: str):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_file_key
        self.__path_file_key = path_file_key

    def check_env_auth_credential(self) -> bool:
        pass


def check_valid_path(path_file_key):
    if pathlib.Path.is_file(path_file_key):
        return True
    return False


def main():
    setting = CloudStorageSetting()
    setting.set_credentials()
    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()
    bucket = storage_client.create_bucket("figthing-temptation")

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    for bucket in buckets:
        print(bucket)


if __name__ == "__main__":
    main()
