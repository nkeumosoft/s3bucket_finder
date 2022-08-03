"""
    Author: Edmond Ghislain MAKOLLE

"""
from dataclasses import dataclass


@dataclass
class Bucket:
    """S3 Bucket class definition."""

    __name: str
    __access_browser: str
    __location: str
    __url: str
    __acl_found = {
        "Owner_ID": "",
        "private": False,
        "public-read": False,
        "public-read-write": False,
        "aws-exec-read": False,
        "authenticated-read": False,
        "log-delivery-write": False,
    }

    @property
    def get_name(self):
        """Return the bucket name.

        :return: str
        """
        return self.__name

    @property
    def get_access_browser(self):
        """Return the bucket access browser status.

        :return: str
        """
        return self.__access_browser

    @property
    def get_location(self):
        """Return the bucket location.

        :return: str
        """
        return self.__location

    @property
    def get_url(self):
        """Return the bucket link.

        :return: str
        """
        return self.__url

    @property
    def acl_found(self):
        """Return the acl property of a bucket.

        :return: str
        """

        return self.__acl_found

    @acl_found.setter
    def acl_found(self, acl_found):
        """Set the acl properties of a bucket.

        :return: str
        """
        self.__acl_found = acl_found
