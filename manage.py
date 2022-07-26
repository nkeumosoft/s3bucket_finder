import logging
import os
import boto3
from botocore.exceptions import ClientError
import csv
from pathlib import Path


def make_a_csv_file(header_file, data):
    home = str(Path.home())
    folder = os.path.join(home, "ResultsCSV")
    if not os.path.isdir(folder):
        os.mkdir(folder)

    with open(folder + "/rapport_aws_s3.csv", 'w', encoding='UTF-8') as file:
        writer = csv.DictWriter(file, fieldnames=header_file)
        # Use writerows() not writerow()
        writer.writeheader()
        writer.writerows(data)


def human_read_acl(acl):
    result_permissions = {
        "Owner_ID": '',
        "bucket_name": '',
        'url': '',
        'private': False,
        'public-read': False,
        'public-read-write': False,
        'aws-exec-read': False,
        'authenticated-read': False,
        'log-delivery-write': False
    }

    type_permission = {

    }

    if len(acl['Grants']) == 1:
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

            try:

                if type_permission["READ"] and type_permission["WRITE"]:
                    result_permissions['public-read-write'] = True
                elif type_permission["READ"] and not type_permission["WRITE"]:
                    result_permissions['public-read'] = True
            except KeyError as e:
                pass

        result_permissions["Owner_ID"] = acl["Owner"]["ID"]

    return result_permissions


def scan_single_bucket(bucket_name, region_name):
    s3_client = boto3.client('s3')

    try:
        val = s3_client.head_bucket(Bucket=bucket_name)
        acl = s3_client.get_bucket_acl(Bucket=bucket_name)

        dict_acl_permission = human_read_acl(acl)
        dict_acl_permission['bucket_name'] = bucket_name
        dict_acl_permission['url'] = f"https://{bucket_name}.s3.{region_name}.amazonaws.com/"

        return dict_acl_permission
    except ClientError as e:

        if e.response['Error']['Code'] == '404':
            logging.warning('bucket not found')

    return None
