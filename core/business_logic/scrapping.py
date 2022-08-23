"""
    Author: Edmond Ghislain MAKOLLE

"""
import logging
import os
from pathlib import Path
from typing import List, Optional

import xmltodict
from requests import get

from core.business_logic.bucket import Bucket

URL = "https://s3.amazonaws.com"
logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)


def is_status_200(bucket_name: str, location: str, endpoint: str) -> Bucket:
    """Log and return the bucket for the request status code 200.

    :param bucket_name: (String) name of the scrapped bucket.
    :param location: (String) location of the bucket storage.
    :param endpoint: (String) access url of the bucket.
    :return: Bucket
    """
    bucket = Bucket(bucket_name, "Public", location, endpoint)
    logging.info(bucket)
    return bucket


def is_status_403(bucket_name: str, location: str, endpoint: str) -> Bucket:
    """Log and return the bucket for the request status code 403.

    :param bucket_name: (String) name of the scrapped bucket.
    :param location: (String) location of the bucket storage.
    :param endpoint: (String) access url of the bucket.
    :return: Bucket
    """
    bucket = Bucket(bucket_name, "Private", location, endpoint)
    logging.info(bucket)
    return bucket


def is_status_301(data, bucket_name: str) -> Optional[Bucket]:
    """Log and return the bucket for the request status code 301.

    :param data: (Any) data content of a request.
    :param bucket_name: (String) name of the scrapped bucket.
    :return: Bucket | None
    """
    endpoint = data["Error"]["Endpoint"]
    try:
        response = get(f"https://{endpoint}")

        if response.status_code == 200:
            return is_status_200(bucket_name, "US", f"https://{endpoint}")

        else:
            return is_status_403(bucket_name, "US", f"https://{endpoint}")

    except ConnectionError:
        logging.warning(
            f"Connection error for the scan of "
            f"bucket <{bucket_name}> (status=301)."
            f"Check your connexion and restart."
        )
    return None


def is_status_400(data, bucket_name: str) -> Optional[Bucket]:
    """Log and return the bucket for the request status code 400.

    :param data: (Any) data content of a request.
    :param bucket_name: (String) name of the scrapped bucket.
    :return: Bucket | None
    """
    error = data["Error"]
    if error["Code"] == "IllegalLocationConstraintException":
        location = error["Message"].split(" ")[1]
        url = f"https://s3.{location}.amazonaws.com/{bucket_name}"
        try:
            response = get(url)

            if response.status_code == 200:
                return is_status_200(bucket_name, location, url)
            else:
                return is_status_403(bucket_name, location, url)

        except ConnectionError:
            logging.warning(
                f"Connection error for the scan of "
                f"bucket <{bucket_name}> (status=400)."
                f"Check your connexion and restart."
            )

    else:
        logging.error(f"Invalid bucket name <{bucket_name}>")
        return None

    return None


def scrapping(bucket_name: str) -> Optional[Bucket]:
    """Checks the existence of the bucket name and provides information.

    :param bucket_name: (String) Represent the name of bucket.
    :return: Bucket | None
    """
    try:
        response = get(URL + "/" + bucket_name)

        if response.status_code == 200:
            return is_status_200(bucket_name, "US", URL + "/" + bucket_name)

        data = xmltodict.parse(response.content)

        if response.status_code in (400, 403, 404):
            if response.status_code == 400:
                return is_status_400(data, bucket_name)

            elif response.status_code == 403:
                return is_status_403(
                    bucket_name, "US", URL + "/" + bucket_name
                )

            else:
                logging.info(f"Bucket <{bucket_name}> || Don't Exist")
                return None

        if response.status_code == 301:
            return is_status_301(data, bucket_name)

    except ConnectionError:
        logging.warning(
            f"Connection error for the scan of bucket "
            f"<{bucket_name}>. Check your connexion and restart."
        )
    return None


def check_file_exist(file: str) -> bool:
    """Checks if the file or the path to the file in parameter exists.

    :param file: (String) file name or path to check.
    :return: Boolean
    """
    if "/" in file:
        return Path(file).is_file()
    else:
        return Path(os.path.join(os.getcwd(), file)).is_file()


def scrapping_file(file: str) -> Optional[List[Bucket]]:
    """Checks the existence of buckets which are on a file and provides their
    public properties.

    :param file: (Any) name or path of file containing a list of buckets
     names.
    :return: list[Bucket] | None
    """
    buckets = []

    if check_file_exist(file):
        with open(file, "r") as _file:
            for bucket_name in _file.readlines():
                bucket = scrapping(bucket_name.rstrip("\n"))
                if bucket is not None:
                    buckets.append(bucket)
            return buckets

    else:
        logging.error("This path or file don't exist !")
        return None
