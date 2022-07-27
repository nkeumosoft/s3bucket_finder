import logging
import os
import csv
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
import xmltodict
import requests

from config import setup_config, get_region

# some errors of aws

PermanentRedirect = 'PermanentRedirect'
AccessDenied = 'AccessDenied'
NoSuchBucket = 'NoSuchBucket'
IllegalLocationConstraintException = 'IllegalLocationConstraintException'

# type of response
ListBucketResult = 'ListBucketResult'
Error = 'Error'

RGN_NAME = ["us-east-2", "us-east-1", "us-west-1", "us-west-2", "af-south-1", "ap-south-1", "ap-northeast-3",
            "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-northeast-1", "ca-central-1", "eu-central-1",
            "eu-west-1", "eu-west-2", "eu-west-3", "eu-south-1", "eu-west-3", "me-south-1", "sa-east-1"]


class S3WebScrapping:
    file_name = ''
    host = ''
    page = ''

    def __init__(self, filename):
        self.initial_region = get_region()
        self.file_name = filename

        self.page = self.load_bucket_names_from_file()
        self.indice_region = -1
        self.content_make_to_csv = []

    def __exit__(self):
        setup_config(self.initial_region)

    def get_single_aws_site(self, url):

        """
            check if bucket name exist
            :param str host the url of amazone

            :return dictionnary { 'location': ,'status: }

        """
        try:

            return_date = {
                'location': url,
                'status': '',
            }

            logging.warning(url)
            response = requests.get(url=url)
            dict_data = xmltodict.parse(response.content)

            if ListBucketResult in dict_data:

                return_date['status'] = ListBucketResult
                return return_date
            else:
                erro_type = dict_data['Error']
                if erro_type['Code'] == AccessDenied:

                    return_date['status'] = AccessDenied
                    #  check if auth user have access else is private
                    return return_date
                elif erro_type['Code'] == PermanentRedirect:

                    url = f"https://{erro_type['Endpoint']}"
                    return self.get_single_aws_site(url)
                elif erro_type['Code'] == IllegalLocationConstraintException:

                    region = erro_type['Message'].split(' ')
                    sub_url = url.find('.s3.')
                    url = f"{url[:sub_url+4]+region[1]}.amazonaws.com"

                    return self.get_single_aws_site(url)
                elif erro_type['Code'] == NoSuchBucket:

                    return_date['status'] = NoSuchBucket
                    return return_date



        except requests.exceptions.RequestException as e:
            logging.error('ici', e)
            pass
        return ''

    def get_aws_s3_site(self):
        list_bucket = []
        for word in self.page:
            url = f'http://{word}.s3.amazonaws.com'
            xmldictdoc = self.get_single_aws_site(url)

            if 'status' in xmldictdoc and not NoSuchBucket == xmldictdoc['status']:
                list_bucket.append({'bucket_name': word, 'url': xmldictdoc['location'], 'status':xmldictdoc['status'] })
        logging.warning(list_bucket)
        self.content_make_to_csv = self.list_parse_result(list_bucket)

    def list_parse_result(self, list_bucket):
        result_liste_des_buckets = []
        tmp_bucket = None
        for bucket in list_bucket:
            tmp_bucket = self.parse_result(bucket['bucket_name'], bucket['url'])
            logging.warning(bucket)
            if 'status' in bucket:

                tmp_bucket['access url'] = bucket['status']
                result_liste_des_buckets.append(tmp_bucket)

        return result_liste_des_buckets

    def human_read_acl(self, acl, access=ListBucketResult):
        result_permissions = {
            "Owner_ID": '',
            "bucket_name": '',
            'url': '',
            'private': False,
            'public-read': False,
            'public-read-write': False,
            'aws-exec-read': False,
            'authenticated-read': False,
            'log-delivery-write': False,
            'access url':'',
        }

        type_permission = {

        }

        if len(acl['Grants']) == 1 or access == AccessDenied:
            result_permissions = {
                "Owner_ID": '',
                "bucket_name": '',
                'url': '',
                'private': True,
                'public-read': False,
                'public-read-write': False,
                'aws-exec-read': False,
                'authenticated-read': False,
                'log-delivery-write': False

            }
        else:
            for grant in acl['Grants']:
                try:
                    if grant['Grantee']['URI'] == "http://acs.amazonaws.com/groups/global/AllUsers":
                        type_permission['URI'] = "http://acs.amazonaws.com/groups/global/AllUsers"
                        if grant['Permission'] == 'READ':
                            type_permission['READ'] = 'READ'
                        else:
                            type_permission['WRITE'] = 'WRITE'
                    elif grant['Grantee']['URI'] == "http://acs.amazonaws.com/groups/global/AuthenticatedUsers":
                        result_permissions['authenticated-read'] = True
                    elif grant['Grantee']['URI'] == "http://acs.amazonaws.com/groups/s3/LogDelivery":
                        result_permissions['log-delivery-write'] = True
                except KeyError as e:
                    pass

            if type_permission["READ"] and type_permission["WRITE"]:
                result_permissions['public-read-write'] = True
            elif type_permission["READ"] and not type_permission["WRITE"]:
                result_permissions['public-read'] = True

            result_permissions["Owner_ID"] = acl["Owner"]["ID"]

        return result_permissions

    def parse_result(self, bucket_name, url, region='us‑east‑1'):
        dict_acl_permission = {
            "Owner_ID": '',
            "bucket_name": '',
            'url': '',
            'private': True,
            'public-read': False,
            'public-read-write': False,
            'aws-exec-read': False,
            'authenticated-read': False,
            'log-delivery-write': False,
            'access url':'',
        }
        s3_client = boto3.client('s3')
        acl = {'Grants': {}}
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            acl = s3_client.get_bucket_acl(Bucket=bucket_name)


            dict_acl_permission = self.human_read_acl(acl)
            dict_acl_permission['bucket_name'] = bucket_name
            dict_acl_permission['url'] = url
            #logging.warning(dict_acl_permission)
            return dict_acl_permission
        except ClientError as e:
            logging.error('code errors: '+e.response['Error']['Code'])
            if e.response['Error']['Code'] == '403':
                dict_acl_permission['bucket_name'] = bucket_name
                dict_acl_permission['url'] = url

            if e.response['Error']['Code'] == AccessDenied:
                dict_acl_permission = self.human_read_acl(acl, access=AccessDenied)
                dict_acl_permission['bucket_name'] = bucket_name
                dict_acl_permission['url'] = url
                logging.warning(dict_acl_permission)
                logging.warning(bucket_name + ': ' + AccessDenied )
                dict_acl_permission['access url'] = AccessDenied
                return dict_acl_permission
                #  check if auth user have access else is private

            if e.response['Error']['Code'] == IllegalLocationConstraintException:

                logging.warning(bucket_name + ': ' + IllegalLocationConstraintException)
                self.indice_region += 1
                if self.indice_region <= len(RGN_NAME) - 1:
                    logging.warning(RGN_NAME[self.indice_region])
                    setup_config(RGN_NAME[self.indice_region])
                    self.parse_result(bucket_name, url, region)

            # setup_config
            elif e.response['Error']['Code'] == '404':
                logging.warning('bucket not found', NoSuchBucket)

        return dict_acl_permission

    def load_bucket_names_from_file(self):
        """
        Load in bucket names from a text file

        :param str file_name: Path to text file
        :return: set: All lines of text file
        """
        buckets = set()
        if os.path.isfile(self.file_name):
            with open(self.file_name, 'r') as f:
                for line in f:
                    line = line.rstrip()  # Remove any extra whitespace
                    buckets.add(line)
            return buckets
        else:
            print("Error: '%s' is not a file" % self.file_name)
            exit1 = exit(1)

    def dict_to_csv(self, header_file):

        home = str(Path.home())
        folder = os.path.join(home, "ResultsCSV")
        if not os.path.isdir(folder):
            os.mkdir(folder)

        with open(folder + "/rapport_aws_s3.csv", 'w', encoding='UTF-8') as file:
            writer = csv.DictWriter(file, fieldnames=header_file)
            # Use writerows() not writerow()
            writer.writeheader()
            writer.writerows(self.content_make_to_csv)


#  formatage en console

import argparse


class CustomFormatter(argparse.RawTextHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


def main(CURRENT_VERSION="1.0"):
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Bscan: scan the bucket and make a file for each bucket',
                                     prog='Bscan', allow_abbrev=True, formatter_class=CustomFormatter)
    # Declare arguments
    parser.add_argument('--version', action='version', version=CURRENT_VERSION,
                        help='Display the current version of this tool')

    parser.add_argument('--buckets-file', '-f', dest='aws_file_name',
                        help='Name of text file containing bucket names to check', metavar='file')
    region = {
        "ie": 'https://s3-eu-west-1.amazonaws.com',
        "nc": 'https://s3-us-west-1.amazonaws.com',
        "us": 'https://s3.amazonaws.com',
        "si": 'https://s3-ap-southeast-1.amazonaws.com',
        "to": 'https://s3-ap-northeast-1.amazonaws.com'}
    # Parse the args
    args = parser.parse_args()

    field_head = [
        "Owner_ID",
        "bucket_name",
        'url',
        "private",
        "public-read",
        "public-read-write",
        "aws-exec-read",
        "authenticated-read",
        'log-delivery-write',
        'access url',

    ]

    if args.aws_file_name is not None:
        bucketsIn = args.aws_file_name
        print(bucketsIn)
        aws_s3_web = S3WebScrapping(bucketsIn)
        aws_s3_web.get_aws_s3_site()
        aws_s3_web.dict_to_csv(field_head)


if __name__ == '__main__':
    main()
