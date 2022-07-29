"""
    create a bucket class with the respect of solid principle

"""


class Bucket:
    __name: str = ''
    __access_browser: bool = True
    __location: str = ''
    __url: str = ''
    foundACL = None

    def __init__(self, name: str, access_browser: bool,
                 location: str, url: str):
        self.__name = name
        self.__access_browser = access_browser
        self.__location = location
        self.__url = url
        self.__foundACL = None

    def get_name(self):
        return self.__name

    def get_access_browser(self):
        return self.__access_browser

    def get_location(self):
        return self.__location

    def get_url(self):
        return self.__url

    def set_location(self, location):
        self.__location = location

    def set_url(self, url):
        self.__url = url

    def set_name(self, name):
        self.__name = name

    def set_access_browser(self, access_browser):
        self.__access_browser = access_browser


