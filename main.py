import argparse
import logging
from requests.exceptions import ConnectionError

import boto3
from botocore.exceptions import NoCredentialsError

from models.service import S3Acl, display_bucket_to_dict
from models.aws_setting import AwsSetting
from utils.createcsvfile import make_bucket_result_to_csv
from utils.scapping import scrapping, scrapping_buckets


def main():
    settings = AwsSetting()

    parser = argparse.ArgumentParser(
        description="s3bucket_finder: Analysis of "
                    "Buckets by AfroCode\n", prog="s3bucket_finder",
        allow_abbrev=False)
    parser.add_argument('-s', '--scrap-bucket', dest='bucket_name',
                        help='Scan the bucket, if exist, and provide public '
                             'properties')
    parser.add_argument('-sf', '--scrap-file', dest='file',
                        help='Scan a file containing a list of buckets name, '
                             'and provide public properties. You can '
                             'give the name of file if is on the current '
                             'directory, of give the path of the file')

    subparsers = parser.add_subparsers(title='mode', dest='mode')

    # Download Mode
    parser_download = subparsers.add_parser(
        'download',
        help="Create a csv file who  content the buckets information "
             "with acl property")
    parser_download.add_argument(
        '--rename', '-r', dest='rename',
        help="Rename the output file the Default name "
             "is <<rapport_aws_s3.csv>>",
        required=False)

    # Setup Config Mode
    parser_config = subparsers.add_parser('setup-config',
                                          help="Local AWS Configuration of "
                                               "config file")
    parser_config.add_argument('--region', '-r', dest='region',
                               help='Name of the AWS region.', required=True)
    parser_config.add_argument('--output', '-o', dest='output',
                               help='Name of the AWS CLI output format. '
                                    'Default: json', default='json')

    # Setup Credentials Mode
    parser_cred = subparsers.add_parser('setup-cred',
                                        help="Local AWS Configuration of "
                                             "credentials file")
    parser_cred.add_argument('--id', '-i', dest='aws_access_key_id',
                             help='Represents the AWS Access Key Id.',
                             required=True)
    parser_cred.add_argument('--key', '-k', dest='aws_secret_access_key',
                             help='Represents the AWS Secret Access Key',
                             required=True)

    # Parse the args
    args = parser.parse_args()
    list_of_bucket = ''
    if args.bucket_name is not None:
        list_of_bucket = scrapping(args.bucket_name)

    if args.file is not None:
        list_of_bucket = scrapping_buckets(args.file)

    if args.mode == 'setup-config':
        if args.output != 'json':
            settings.setup_config(region=args.region, output=args.output)
        else:
            settings.setup_config(region=args.region)
        # Modify print by logging
        print("Configuration of the config file done.")
    elif args.mode == 'setup-cred':
        settings.setup_credentials(id=args.aws_access_key_id,
                                   key=args.aws_secret_access_key)
        # Modify print by logging
        print("Configuration of the credentials file done.")

    if args.mode == 'download' and (args.bucket_name is not None or args.file):
        field_name = [
            'Owner_ID',
            'bucket_name',
            'access browser',
            'url',
            'private',
            'public-read',
            'public-read-write',
            'aws-exec-read',
            'authenticated-read',
            'log-delivery-write',

        ]
        if args.rename is not None:
            file_output = args.rename
        else:
            file_output = "rapport_aws_s3"
        try:
            fraud_detector = boto3.client('sts')
            fraud_detector.get_caller_identity()
            aws_s3_client = boto3.client('s3')
            aws_s3_acl = S3Acl(list_of_bucket, aws_s3_client, settings)

            if args.bucket_name is not None:

                bucket_acl_value = aws_s3_acl.get_bucket_acl(list_of_bucket)
                dict_to_save_csv = display_bucket_to_dict(bucket_acl_value)
                print(dict_to_save_csv)
                make_bucket_result_to_csv([dict_to_save_csv], field_name,
                                          file_name=file_output)
            else:
                dict_to_save_csv = []
                aws_s3_acl.get_acl_list_of_bucket()
                list_of_bucket = aws_s3_acl.list_of_bucket

                for bucket in list_of_bucket:
                    tmp_bucket = display_bucket_to_dict(bucket)
                    print(tmp_bucket)
                    dict_to_save_csv.append(tmp_bucket)

                make_bucket_result_to_csv(
                    dict_to_save_csv,
                    field_name,
                    file_name=file_output)

        except NoCredentialsError:
            print('please make sure that you have a aws credential  config '
                  'before use this command ')
        except Exception as e:
            logging.error(e)
        except ConnectionError:
            print('connection not found')
    else:
        print(' args not found  ')
        exit(-1)


if __name__ == '__main__':
    main()
