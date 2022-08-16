"""
    Author: Noutcheu Libert Joran

"""

import logging

from botocore.exceptions import ClientError

from core.aws.aws_setting import AwsSetting
from core.business_logic.bucket import Bucket
from core.business_logic.exception import RGN_NAME, Permission, TypeException


class S3Acl:
    """A class to represent aws service to check acl property for a bucket."""

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
        self.initial_region = aws_settings.region

    def __exit__(self, exception_type, exception_value, traceback):
        self.__aws_setting.config = (self.initial_region,)

    def check_head_bucket(self, bucket: Bucket) -> bool:
        """check if bucket exist.

        :param bucket: bucket to check in aws s3 storage
        """

        try:
            if not isinstance(bucket, Bucket):
                raise ValueError("you must send a bucket object")

            self.aws_client.head_bucket(Bucket=bucket.get_name)
        except ClientError as error:
            resp_error = error.response
            if resp_error.get("Error").get("Code") == "404":
                logging.error("bucket not %s found", bucket.get_name)
                return False

        except ValueError:
            logging.error("you must send a bucket object")
            exit(0)
        return True

    def check_read_acl_permissions(self, bucket):
        """Check if we have a permission to read a bucket.

        :param bucket: a bucket to get the acl permission
        and check it
        :return dict
        """

        s3_client = self.aws_client
        acl_perm_response = {
            "permission": Permission.ACCESS_DENIED,
            "acl_property": None,
        }

        if self.check_head_bucket(bucket):

            try:

                acl_properties = s3_client.get_bucket_acl(
                    Bucket=bucket.get_name
                )

                acl_perm_response = {
                    "permission": Permission.LIST_BUCKET_RESULT,
                    "acl_property": acl_properties,
                }

                return acl_perm_response

            except ClientError as aws_error:
                aws_resp = aws_error.response
                if (aws_resp.get("Error").get("Code") == "AccessDenied") or (
                    aws_resp.get("Error").get("Code") == "AllAccessDisabled"
                ):
                    acl_perm_response["permission"] = Permission.ACCESS_DENIED
                elif (
                    aws_resp.get("Error").get("Code")
                    == TypeException.ILLEGAL_LOCATION
                ):
                    acl_perm_response[
                        "permission"
                    ] = "LocationConstraintException"

            return acl_perm_response
        return None

    def get_acl_list_of_bucket(self) -> None:
        """get a bucket acl property for a list of bucket."""
        logging.info(self.list_of_bucket)
        for bucket in self.list_of_bucket:
            logging.info(bucket)
            self.get_bucket_acl(bucket)

    def get_bucket_acl(self, bucket, region="us‑east‑1") -> Bucket:
        """get a bucket acl property for on  bucket.

        :param bucket: Bucket
        :param region: str the region of a bucket
        :return bucket: for a single file
        """

        try:
            responses_of_read_acl = self.check_read_acl_permissions(bucket)

            if responses_of_read_acl["permission"] == Permission.ACCESS_DENIED:
                acl: dict = {"Grants": {}}

                bucket.acl_found = list_of_bucket_human_read_acl(
                    acl, Permission.ACCESS_DENIED
                )

            elif (
                responses_of_read_acl["permission"]
                == Permission.LIST_BUCKET_RESULT
            ):
                bucket.acl_found = list_of_bucket_human_read_acl(
                    responses_of_read_acl["acl_property"],
                    Permission.LIST_BUCKET_RESULT,
                )

            else:
                # if the access it is not allow or denied
                # then  the region  is not good, and we change it
                self.indice_region += 1
                if self.indice_region <= len(RGN_NAME) - 1:
                    self.__aws_setting.config = (RGN_NAME[self.indice_region],)
                    self.get_bucket_acl(bucket, region)

        except ClientError as aws_error:

            logging.error(aws_error)
        return bucket


def list_of_bucket_human_read_acl(
    acl: dict, access=Permission.LIST_BUCKET_RESULT
):
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

    # check if the bucket is private
    if len(acl["Grants"]) == 1 or access == Permission.ACCESS_DENIED:
        result_permissions["private"] = True

        return result_permissions

    # for any element in grant check if bucket acl is

    # public-read public read and write or user authentication

    for grant in acl["Grants"]:
        try:
            if grant.get("Grantee").get("Type") == "Group":
                result_permissions = display_acl_properties(
                    grant, result_permissions
                )

        except KeyError:
            pass

    result_permissions["Owner_ID"] = acl["Owner"]["ID"]

    return result_permissions


def display_acl_properties(grant: dict, result_permissions: dict) -> dict:
    """"""

    acl_url = grant["Grantee"]["URI"]
    if acl_url == "http://acs.amazonaws.com/groups/global/AllUsers":
        result_permissions = access_control_unauthenticated_user(
            result_permissions, grant
        )

    result_permissions["authenticated-read"] = (
        acl_url == "http://acs.amazonaws.com/groups/global/AuthenticatedUsers"
    )

    result_permissions["log-delivery-write"] = (
        acl_url == "http://acs.amazonaws.com/groups/s3/LogDelivery"
    )

    return result_permissions


def access_control_unauthenticated_user(
    result_permissions, permission
) -> dict:
    """"""
    result_permissions["public-read-write"] = (
        permission["Permission"] == "FULL_CONTROL"
    )
    result_permissions["public-read"] = permission["Permission"] == "READ"
    result_permissions["public-read-acp"] = (
        permission["Permission"] == "READ_ACP"
    )
    result_permissions["public-write"] = permission["Permission"] == "WRITE"
    result_permissions["public-write-acp"] = (
        permission["Permission"] == "WRITE_ACP"
    )

    return result_permissions


def display_bucket_to_dict(bucket: Bucket) -> dict:
    """
    transform a bucket attribute in to dict element to save easily into
    csv files
    :param: bucket: Bucket
    :return field_head:dict
    """
    field_head: dict = {
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
