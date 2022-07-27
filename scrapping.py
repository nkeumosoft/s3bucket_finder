import os.path
from pathlib import Path

import xmltodict
import requests


def scrapping(bucket_name: str) -> None:
    """
    Checks the existence of the bucket entered as a parameter and provides the public properties.

    :param bucket_name: (String) The name of the scanning bucket.
    :return: None
    """
    url = "https://s3.amazonaws.com"

    try:
        response = requests.get(url + "/" + bucket_name)
        data = xmltodict.parse(response.content)
        if response.status_code == 200:
            print(f"Bucket <{bucket_name}> || Exist || Public || US Location || {url}/{bucket_name}")
        else:
            if response.status_code == 403:
                print(f"Bucket <{bucket_name}> || Exist || Private || US Location || {url}/{bucket_name}")

            elif response.status_code == 400:
                error = data['Error']
                message = error['Message']
                location = message.split(" ")[1]
                uri = f"https://s3.{location}.amazonaws.com/{bucket_name}"
                try:
                    request = requests.get(uri)
                    if request.status_code == 200:
                        print(f"Bucket <{bucket_name}> || Exist || Public || {location} Location || {uri}")
                    else:
                        print(f"Bucket <{bucket_name}> || Exist || Private || {location} Location || {uri}")

                except ConnectionError:
                    print(f"Connection Error ==> in status code 400 for bucket {bucket_name}")

            elif response.status_code == 301:
                error = data['Error']
                endpoint = error['Endpoint']
                try:
                    request = requests.get(f"https://{endpoint}")
                    if request.status_code == 200:
                        print(f"Bucket <{bucket_name}> || Exist || Public || US Location || https://{endpoint}")
                    else:
                        print(f"Bucket <{bucket_name}> || Exist || Private || US Location || https://{endpoint}")
                except ConnectionError:
                    print(f"Connection Error ==> in status code 301 for bucket {bucket_name}")

            elif response.status_code == 404:
                print(f"Bucket <{bucket_name}> || Don't Exist")
    except ConnectionError:
        print("Connection Error")


def scrapping_buckets(file):
    """
    Checks the existence of buckets which are on a file and provides their public properties.

    :param file: (Any) A file containing a list of buckets names.
    :return: None
    """
    if "/" in str(file):
        file_exist = Path(file).is_file()
    else:
        file_path = os.path.join(os.getcwd(), file)
        print(file_path)
        file_exist = Path(file_path).is_file()

    if file_exist:
        with open(file, "r") as f:
            for bucket in f.readlines():
                scrapping(bucket.rstrip("\n"))
    else:
        print("This path or file don't exist !")
