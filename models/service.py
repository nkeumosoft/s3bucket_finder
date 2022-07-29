import logging

from botocore.exceptions import ClientError

from models.bucket import Bucket
from models.s3exception import Permission, TypeException, RGN_NAME
from models.aws_setting import AwsSetting


class S3Acl:

    def __init__(self, list_of_bucket: Bucket, aws_s3_client,
                 aws_settings: AwsSetting):
        self.list_of_bucket = list_of_bucket
        self.aws_client = aws_s3_client
        self.__aws_setting = aws_settings
        self.indice_region = -1
        self.initial_region = self.__aws_setting.get_region()

    def __exit__(self):
        self.__aws_setting.setup_config(self.initial_region)

    def get_acl_list_of_bucket(self) -> None:
        for bucket in self.list_of_bucket:
            self.get_bucket_acl(bucket)

    def get_bucket_acl(self, bucket, region='us‑east‑1'):
        name = bucket.get_name()

        access_browser = bucket.get_access_browser()
        s3_client = self.aws_client
        acl = {'Grants': {}}

        try:

            s3_client.head_bucket(Bucket=name)
            acl = s3_client.get_bucket_acl(Bucket=name)

            bucket.set_acl_found(bucket_human_read_acl(acl, access_browser))

            # logging.warning(dict_acl_permission)
            return bucket
        except ClientError as e:

            #  check if auth user have access else they access is private
            if e.response['Error']['Code'] == '403' or \
                    e.response['Error']['Code'] == Permission.AccessDenied:

                bucket.set_acl_found(
                    bucket_human_read_acl(acl, Permission.AccessDenied)
                    )

            logging.warning(TypeException.IllegalLocationConstraintException)
            if e.response['Error']['Code'] \
                    == TypeException.IllegalLocationConstraintException:

                logging.warning(e.response['Error']['Code'])
                self.indice_region += 1
                if self.indice_region <= len(RGN_NAME) - 1:
                    logging.warning(RGN_NAME[self.indice_region])
                    self.__aws_setting.setup_config(
                        RGN_NAME[self.indice_region])
                    self.get_bucket_acl(bucket, region)

            # setup_config
            elif e.response['Error']['Code'] == '404':
                logging.warning('bucket not found', Permission.NoSuchBucket)

        return bucket


def bucket_human_read_acl(acl: dict, access=Permission.ListBucketResult):
    """      human readable acl properties
             :params  acl:dict
             :params access browser property access
             :return
        """

    result_permissions = {
        'Owner_ID': '',
        'private': False,
        'public-read': False,
        'public-read-write': False,
        'aws-exec-read': False,
        'authenticated-read': False,
        'log-delivery-write': False,
    }

    type_permission = {
        'READ': None,
        'WRITE': None,
    }
    # verifed if the bucket is private
    if len(acl['Grants']) == 1 or access == Permission.AccessDenied:
        logging.warning(Permission.AccessDenied)
        result_permissions = {
            'Owner_ID': '',
            'private': True,
            'public-read': False,
            'public-read-write': False,
            'aws-exec-read': False,
            'authenticated-read': False,
            'log-delivery-write': False

        }
    else:
        # for any element in grant check if bucket acl is
        # public-read public read and write or user authentication

        for grant in acl['Grants']:
            try:
                if grant['Grantee']['URI'] \
                        == "http://acs.amazonaws.com/groups/global/AllUsers":

                    type_permission['URI'] \
                        = "http://acs.amazonaws.com/groups/global/AllUsers"

                    if grant['Permission'] == 'READ':
                        type_permission['READ'] = 'READ'
                    else:
                        type_permission['WRITE'] = 'WRITE'
                elif grant['Grantee'][
                    'URI'] == "http://acs.amazonaws.com/groups/global/" \
                              "AuthenticatedUsers":
                    result_permissions['authenticated-read'] = True
                elif grant['Grantee'][
                    'URI'] == "http://acs.amazonaws.com/groups/s3/" \
                              "LogDelivery":
                    result_permissions['log-delivery-write'] = True
            except KeyError as e:
                pass

        if type_permission["READ"] and type_permission["WRITE"]:
            result_permissions['public-read-write'] = True
        elif type_permission["READ"] and not type_permission["WRITE"]:
            result_permissions['public-read'] = True

        result_permissions['Owner_ID'] = acl["Owner"]["ID"]

    return result_permissions


def display_bucket_to_dict(bucket: Bucket) -> dict:
    field_head = {
        'Owner_ID': str(bucket.get_acl_found()["Owner_ID"]),
        'bucket_name': bucket.get_name(),
        'access browser': bucket.get_access_browser(),
        'url': bucket.get_url(),

        'private': bucket.get_acl_found()["private"],
        'public-read': bucket.get_acl_found()["public-read"],
        'public-read-write': bucket.get_acl_found()["public-read-write"],
        'aws-exec-read': bucket.get_acl_found()["aws-exec-read"],
        'authenticated-read': bucket.get_acl_found()["authenticated-read"],
        'log-delivery-write': bucket.get_acl_found()["log-delivery-write"],

    }
    return field_head
