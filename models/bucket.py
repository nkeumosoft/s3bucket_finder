"""
    Author: Edmond Ghislain MAKOLLE

"""


class Bucket:
    """
    S3 Bucket class definition.
    """

    def __init__(self, name: str, access_browser: str, location: str,
                 url: str):
        self.__name = name
        self.__access_browser = access_browser
        self.__location = location
        self.__url = url

    def get_name(self):
        """
        Return the bucket name.

        :return: str
        """
        return self.__name

    def get_access_browser(self):
        """
        Return the bucket access browser status.

        :return: str
        """
        return self.__access_browser

    def get_location(self):
        """
        Return the bucket location.

        :return: str
        """
        return self.__location

    def get_url(self):
        """
        Return the bucket link.

        :return: str
        """
        return self.__url
