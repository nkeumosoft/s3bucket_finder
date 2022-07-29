from enum import Enum

from bucket import Bucket


class TypeException(Enum):
    PermanentRedirect = 'PermanentRedirect'
    IllegalLocationConstraintException = 'IllegalLocationConstraintException'


class Permission(Enum):

    AccessDenied = 'AccessDenied'
    NoSuchBucket = 'NoSuchBucket'
    ListBucketResult = 'ListBucketResult'


def get_bucket_acl(list_of_bucket: Bucket):
    s3_client = boto3.client('s3')
    acl = {'Grants': {}}
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        acl = s3_client.get_bucket_acl(Bucket=bucket_name)

        dict_acl_permission = self.human_read_acl(acl)
        dict_acl_permission['bucket_name'] = bucket_name
        dict_acl_permission['url'] = url
        # logging.warning(dict_acl_permission)
        return dict_acl_permission
    except ClientError as e:
        logging.error('code errors: ' + e.response['Error']['Code'])
        if e.response['Error']['Code'] == '403':
            dict_acl_permission['bucket_name'] = bucket_name
            dict_acl_permission['url'] = url

        if e.response['Error']['Code'] == AccessDenied:
            dict_acl_permission = self.human_read_acl(
                acl,
                access=AccessDenied)
            dict_acl_permission['bucket_name'] = bucket_name
            dict_acl_permission['url'] = url
            logging.warning(dict_acl_permission)
            logging.warning(bucket_name + ': ' + AccessDenied)
            dict_acl_permission['access url'] = AccessDenied
            return dict_acl_permission
            #  check if auth user have access else is private

        if e.response['Error'][
            'Code'] == IllegalLocationConstraintException:

            logging.warning(
                bucket_name + ': '
                + IllegalLocationConstraintException)
            self.indice_region += 1
            if self.indice_region <= len(RGN_NAME) - 1:
                logging.warning(RGN_NAME[self.indice_region])
                setup_config(RGN_NAME[self.indice_region])
                self.parse_result(bucket_name, url, region)

        # setup_config
        elif e.response['Error']['Code'] == '404':
            logging.warning('bucket not found', NoSuchBucket)

    return dict_acl_permission


def bucket_human_read_acl(acl, access=Permission.ListBucketResult):
    """
          human readable acl properties
         :params  acl acl dictionnary
         :params access browser property access
         :return
    """

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
        'access url': '',
    }

    type_permission = {

    }

    # check if the bucket is private

    if len(acl['Grants']) == 1 or access == Permission.AccessDenied:
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
        # for any element in grant check if bucket acl is
        # public-read public read and write or user authentication
        for grant in acl['Grants']:
            try:
                if grant['Grantee'][
                    'URI'] == "http://acs.amazonaws.com/groups/" \
                              "global/AllUsers":
                    type_permission[
                        'URI'] = "http://acs.amazonaws.com/groups/" \
                                 "global/AllUsers"
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

        result_permissions["Owner_ID"] = acl["Owner"]["ID"]
    return result_permissions
