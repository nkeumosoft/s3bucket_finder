"""
    Author: Noutcheu Libert Joran
"""

from enum import Enum

RGN_NAME = ["us-east-2", "us-east-1", "us-west-1", "us-west-2", "af-south-1",
            "ap-south-1", "ap-northeast-3", "ap-northeast-2",
            "ap-southeast-1", "ap-southeast-2", "ap-northeast-1",
            "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2",
            "eu-west-3", "eu-south-1", "eu-west-3", "me-south-1", "sa-east-1"]


class TypeException(Enum):
    PermanentRedirect = 'PermanentRedirect'
    IllegalLocationConstraintException = 'IllegalLocationConstraintException'


class Permission(Enum):
    AccessDenied = 'AccessDenied'
    NoSuchBucket = 'NoSuchBucket'
    ListBucketResult = 'ListBucketResult'
