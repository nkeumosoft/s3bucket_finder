"""
    Author: Edmond Ghislain MAKOLLE

"""
import os
from pathlib import Path

import requests
import xmltodict

from models.bucket import Bucket


def scrapping(name):
    """
    Checks the existence of the bucket name and provides
    information.

    :param name: (String) Represent the name of bucket.
    :return: Bucket | None
    """
    url = "https://s3.amazonaws.com"

    try:
        response = requests.get(url + "/" + name)
        data = xmltodict.parse(response.content)
        if response.status_code == 200:
            # Modify print by logging
            print(f"Bucket <{name}> || Exist || Public || "   
                  f"US Location || {url}/{name}")
            return Bucket(name=name, access_browser="Public",
                          location="US", url=f"{url}/{name}")

        else:
            if response.status_code == 403:
                # Modify print by logging
                print(f"Bucket <{name}> || Exist || Private || "
                      f"US Location || {url}/{name}")
                return Bucket(name=name, access_browser="Private",
                              location="US", url=f"{url}/{name}")

            elif response.status_code == 400:
                error = data['Error']
                if error['Code'] == "IllegalLocationConstraintException":
                    message = error['Message']
                    location = message.split(" ")[1]
                    uri = f"https://s3.{location}.amazonaws.com/" \
                          f"{name}"
                    try:
                        request = requests.get(uri)
                        if request.status_code == 200:
                            # Modify print by logging
                            print(f"Bucket <{name}> || Exist || "
                                  f"Public || {location} Location || {uri}")
                            return Bucket(name=name, access_browser="Public",
                                          location=location, url=uri)

                        else:
                            # Modify print by logging
                            print(f"Bucket <{name}> || Exist || "
                                  f"Private || {location} Location || {uri}")
                            return Bucket(name=name, access_browser="Private",
                                          location=location, url=uri)

                    except ConnectionError:
                        # Modify print by logging
                        print(f"Connection Error ==> in status code 400 for "
                              f"bucket {name}")
                else:
                    # Modify print by logging
                    print(f"Invalid bucket name <{name}>")
                    return None

            elif response.status_code == 301:
                error = data['Error']
                endpoint = error['Endpoint']
                try:
                    request = requests.get(f"https://{endpoint}")
                    if request.status_code == 200:
                        # Modify print by logging
                        print(f"Bucket <{name}> || Exist || "
                              f"Public || US Location || "
                              f"https://{endpoint}")
                        return Bucket(name=name, access_browser="Public",
                                      location="US",
                                      url=f"https://{endpoint}")

                    else:
                        # Modify print by logging
                        print(f"Bucket <{name}> || Exist || "
                              f"Private || US Location || "
                              f"https://{endpoint}")
                        return Bucket(name=name, access_browser="Private",
                                      location="US",
                                      url=f"https://{endpoint}")

                except ConnectionError:
                    # Modify print by logging
                    print(f"Connection Error ==> in status code 301 for "
                          f"bucket {name}")

            elif response.status_code == 404:
                # Modify print by logging
                print(f"Bucket <{name}> || Don't Exist")
                return None

    except ConnectionError:
        # Modify print by logging
        print("Connection Error")


def scrapping_buckets(file):
    """
    Checks the existence of buckets which are on a file and provides
    their public properties.

    :param file: (Any) A file containing a list of buckets names.
    :return: list[Bucket]
    """
    buckets = []

    if "/" in str(file):
        file_exist = Path(file).is_file()
    else:
        file_path = os.path.join(os.getcwd(), file)
        # Modify print by logging
        print(file_path)
        file_exist = Path(file_path).is_file()

    if file_exist:
        with open(file, "r") as f:
            for bucket_name in f.readlines():
                bucket = scrapping(bucket_name.rstrip("\n"))
                if bucket is not None:
                    buckets.append(bucket)
        return buckets

    else:
        print("This path or file don't exist !")
        return None
