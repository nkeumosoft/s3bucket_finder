"""
    Author: Noutcheu Libert Joran

"""

import logging

from botocore.exceptions import ClientError

from ..aws.aws_local_setting_getter import AwsLocalSettingGetter
from ..aws.aws_setting import AwsSetting
from .bucket import Bucket
from .s3exception import RGN_NAME, Permission, TypeException


class S3Acl:
    """A class to represent  aws service to check acl property for a bucket."""

    def __init__(
        self,
        list_of_bucket: list,
        aws_s3_client,
        aws_settings: AwsSetting,
    ):
        self.list_of_bucket = list_of_bucket
        self.aws_client = aws_s3_client
        self.__aws_setting = aws_settings
        self.indice_region = -1
        self.initial_region = AwsLocalSettingGetter().get_region()

    def __exit__(self, exception_type, exception_value, traceback):
        self.__aws_setting.setup_config(self.initial_region)

    def check_head_bucket(self, bucket: Bucket) -> bool:
        """check if bucket exist.

        :param bucket: bucket to check in aws s3 storage
        """

        if not isinstance(bucket, Bucket):
            raise ValueError("you must send a bucket object")

        try:
            self.aws_client.head_bucket(Bucket=bucket.get_name)
        except ClientError as error:
            if error.response["Error"]["Code"] == "404":
                return False
        return True

    def check_read_acl_permissions(self, bucket):
        """Check if we have a permission to read a bucket.

        :param bucket: a bucket to get the acl permission
        and check it
        :return dict
        """

        s3_client = self.aws_client
        acl_perm_response = {
            "permission": Permission.AccessDenied,
            "acl_property": None,
        }

        if self.check_head_bucket(bucket):
            try:

                acl_properties = s3_client.get_bucket_acl(
                    Bucket=bucket.get_name
                )

                acl_perm_response = {
                    "permission": Permission.ListBucketResult,
                    "acl_property": acl_properties,
                }

                return acl_perm_response

            except ClientError as aws_error:
                if (aws_error.response["Error"]["Code"] == "AccessDenied") or (
                    aws_error.response["Error"]["Code"] == "AllAccessDisabled"
                ):
                    acl_perm_response["permission"] = Permission.AccessDenied
                elif (
                    aws_error.response["Error"]["Code"]
                    == TypeException.IllegalLocationConstraintException
                ):
                    acl_perm_response[
                        "permission"
                    ] = "LocationConstraintException"

            return acl_perm_response
        return None

    def get_acl_list_of_bucket(self) -> None:
        """get a bucket acl property for a list of bucket."""
        for bucket in self.list_of_bucket:
            self.get_bucket_acl(bucket)

    def get_bucket_acl(self, bucket, region="us‑east‑1") -> Bucket:
        """get a bucket acl property for on  bucket.

        :param bucket: Bucket
        :param region: str the region of a bucket
        :return bucket: for a single file
        """

        try:
            responses_of_read_acl = self.check_read_acl_permissions(bucket)
            if responses_of_read_acl["permission"] == Permission.AccessDenied:
                acl: dict = {"Grants": {}}
                bucket.acl_found = bucket_human_read_acl(
                    acl, Permission.AccessDenied
                )
            elif (
                responses_of_read_acl["permission"]
                == Permission.ListBucketResult
            ):
                bucket.acl_found = bucket_human_read_acl(
                    responses_of_read_acl["acl_property"],
                    Permission.ListBucketResult,
                )
            else:
                # if the access it is not allow or denied
                # then  the region  is not good, and we change it
                self.indice_region += 1
                if self.indice_region <= len(RGN_NAME) - 1:
                    self.__aws_setting.setup_config(
                        RGN_NAME[self.indice_region]
                    )
                    self.get_bucket_acl(bucket, region)

        except ClientError as aws_error:
            logging.error(aws_error)
        return bucket


def bucket_human_read_acl(acl: dict, access=Permission.ListBucketResult):
    """transform an Amazon s3 storage bucket acl properties in to human-
    readable.

    :params  acl:dict
    :params access browser property access
    :return
    """

    result_permissions = {
        "Owner_ID": "",
        "private": False,
        "public-read": False,
        "public-read-write": False,
        "public-write-acp": False,
        "public-write": False,
        "public-read-acp": False,
        "aws-exec-read": False,
        "authenticated-read": False,
        "log-delivery-write": False,
    }

    # verifed if the bucket is private
    if len(acl["Grants"]) == 1 or access == Permission.AccessDenied:
        result_permissions["private"] = True
    else:
        # for any element in grant check if bucket acl is
        # public-read public read and write or user authentication

        for grant in acl["Grants"]:
            try:
                if grant["Grantee"]["Type"] == "Group":
                    acl_url = grant["Grantee"]["URI"]
                    if (
                        acl_url
                        == "http://acs.amazonaws.com/groups/global/AllUsers"
                    ):
                        result_permissions = access_control_un_auth_user(
                            result_permissions, grant
                        )

                    elif (
                        acl_url == "http://acs.amazonaws.com/groups/global/"
                        "AuthenticatedUsers"
                    ):
                        result_permissions["authenticated-read"] = True
                    elif (
                        acl_url == "http://acs.amazonaws.com/groups/s3/"
                        "LogDelivery"
                    ):
                        result_permissions["log-delivery-write"] = True
            except KeyError:
                pass

        result_permissions["Owner_ID"] = acl["Owner"]["ID"]

    return result_permissions


def access_control_un_auth_user(result_permissions, permission):
    """"""
    if permission["Permission"] == "FULL_CONTROL":
        result_permissions["public-read-write"] = True
    elif permission["Permission"] == "READ":
        result_permissions["public-read"] = True
    elif permission["Permission"] == "READ_ACP":
        result_permissions["public-read-acp"] = True
    elif permission["Permission"] == "WRITE":
        result_permissions["public-write"] = True
    elif permission["Permission"] == "WRITE_ACP":
        result_permissions["public-write-acp"] = True

    return result_permissions


def display_bucket_to_dict(bucket: Bucket) -> dict:
    """
    transform a bucket attribute in to dict element to save easily into
    csv files
    :param: bucket: Bucket
    :return field_head:dict
    """
    field_head = {
        "bucket_name": bucket.get_name,
        "access browser": bucket.get_access_browser,
        "url": bucket.get_url,
        "Owner_ID": str(bucket.acl_found["Owner_ID"]),
        "ACL: private": bucket.acl_found["private"],
        "ACL: public-read": bucket.acl_found["public-read"],
        "ACL: public-read-write": bucket.acl_found["public-read-write"],
        "ACL: public-write-acp": bucket.acl_found["public-write-acp"],
        "ACL: public-write": bucket.acl_found["public-write"],
        "ACL: public-read-acp": bucket.acl_found["public-read-acp"],
        "ACL: aws-exec-read": bucket.acl_found["aws-exec-read"],
        "ACL: authenticated-read": bucket.acl_found["authenticated-read"],
        "ACL: log-delivery-write": bucket.acl_found["log-delivery-write"],
    }
    return field_head
