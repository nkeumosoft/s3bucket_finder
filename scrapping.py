import xmltodict
import requests


def scrapping(bucket_name: str):
    """
    Checks the existence of the bucket entered as a parameter and provides the public properties.

    :param bucket_name: (String) The name of the scanning bucket.
    :return: None
    """
    url = "https://s3.amazonaws.com"

    response = requests.get(url + "/" + bucket_name)
    data = xmltodict.parse(response.content)

    if data.get('ListBucketResult'):
        print(f"Bucket <{bucket_name}> || Exist || Public || US Location || {url}/{bucket_name}")

    else:
        error = data['Error']
        if error['Code'] == 'AccessDenied':
            print(f"Bucket <{bucket_name}> || Exist || Private || US Location || {url}/{bucket_name}")

        elif error['Code'] == 'IllegalLocationConstraintException':
            message = error['Message']
            location = message.split(" ")[1]
            uri = f"https://s3.{location}.amazonaws.com/{bucket_name}"
            request = requests.get(uri)
            response_data = xmltodict.parse(request.content)
            if response_data.get('ListBucketResult'):
                print(f"Bucket <{bucket_name}> || Exist || Public || {location} Location || {uri}")
            else:
                print(f"Bucket <{bucket_name}> || Exist || Private || {location} Location || {uri}")

        else:
            print(f"Bucket <{bucket_name}> || Don't Exist")


if __name__ == '__main__':
    scrapping("ghislain-bucket")
