"""
    Author: Noutcheu Libert

"""
import logging
import os
import sys

from core.business_logic.setting import GlobalSettings
from utils.createcsvfile import makefolder


class CloudStorageSetting(GlobalSettings):
    __path_file_key: str

    def __init__(self, path_file_key: str = None):

        self.set_credentials(path_file_key)

    def __exit__(self):
        self.save_path_file_key()

    def set_credentials(self, path_file_key):
        if path_file_key and check_valid_path(path_file_key):
            self.path_file_key = path_file_key

    def get_credentials(self):
        if self.__path_file_key is not None:
            return self.__path_file_key

    def load_credentials_from_file(self) -> None:
        logging.info("loading credential json file")
        path = ".google"
        folder_path = makefolder(path)
        if folder_path is not None:
            os.chdir(folder_path)
        config = os.listdir()[0]

        with open(f"{folder_path}/{config}", "r", encoding="utf-8") as file:

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

    @staticmethod
    def check_env_auth_credential(self) -> bool:
        if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
            return True
        return False

    def save_path_file_key(self):
        pass


def check_valid_path(path_file_key):
    if os.path.isfile(path_file_key):
        return True
    return False
