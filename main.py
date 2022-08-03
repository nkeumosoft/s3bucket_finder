import argparse
import logging

import boto3
from botocore.exceptions import NoCredentialsError
from requests.exceptions import ConnectionError

from _utils.createcsvfile import make_csv_with_pandas
from core.aws.aws_setting import AwsSetting
from core.business_logic.scapping import scrapping, scrapping_buckets
from core.business_logic.service import S3Acl, display_bucket_to_dict


def main():
    settings = AwsSetting()
    list_of_bucket = None

    parser = argparse.ArgumentParser(
        description="s3bucket_finder: Analysis of " "Buckets by AfroCode\n",
        prog="s3bucket_finder",
        allow_abbrev=False,
    )
    parser.add_argument(
        "-s",
        "--scrap-bucket",
        dest="bucket_name",
        help="Scan the bucket, if exist, and provide public " "properties",
    )
    parser.add_argument(
        "-sf",
        "--scrap-file",
        dest="file",
        help="Scan a file containing a list of buckets name, "
        "and provide public properties. You can "
        "give the name of file if is on the current "
        "directory, of give the path of the file",
    )

    subparsers = parser.add_subparsers(title="mode", dest="mode")

    # Download Mode
    parser_download = subparsers.add_parser(
        "download",
        help="Create a csv file who  content the buckets information "
        "with acl property",
    )
    parser_download.add_argument(
        "--rename",
        "-r",
        dest="rename",
        help="Rename the output file the Default name "
        "is <<rapport_aws_s3.csv>>",
        required=False,
    )

    # Setup Config Mode
    parser_config = subparsers.add_parser(
        "setup-config", help="Local AWS Configuration of " "config file"
    )
    parser_config.add_argument(
        "--region",
        "-r",
        dest="region",
        help="Name of the AWS region.",
        required=True,
    )
    parser_config.add_argument(
        "--output",
        "-o",
        dest="output",
        help="Name of the AWS CLI output format. " "Default: json",
        default="json",
    )

    # Setup Credentials Mode
    parser_cred = subparsers.add_parser(
        "setup-cred", help="Local AWS Configuration of " "credentials file"
    )
    parser_cred.add_argument(
        "--id",
        "-i",
        dest="aws_access_key_id",
        help="Represents the AWS Access Key Id.",
        required=True,
    )
    parser_cred.add_argument(
        "--key",
        "-k",
        dest="aws_secret_access_key",
        help="Represents the AWS Secret Access Key",
        required=True,
    )

    # Parse the args
    args = parser.parse_args()

    if args.bucket_name is not None:
        list_of_bucket = scrapping(args.bucket_name)

    if args.file is not None:
        list_of_bucket = scrapping_buckets(args.file)

    if args.mode == "setup-config":
        if args.output != "json":
            settings.setup_config(region=args.region, output=args.output)
        else:
            settings.setup_config(region=args.region)
        # Modify print by logging
        print("Configuration of the config file done.")

    elif args.mode == "setup-cred":
        settings.setup_credentials(
            id=args.aws_access_key_id, key=args.aws_secret_access_key
        )
        # Modify print by logging
        print("Configuration of the credentials file done.")

    elif args.mode == "download":

        if args.rename is not None:
            file_output = args.rename
        else:
            file_output = "rapport_aws_s3"

        try:
            aws_s3_client = boto3.client("s3")
            aws_s3_acl = S3Acl(list_of_bucket, aws_s3_client, settings)

            if args.bucket_name is not None:

                aws_s3_acl.check_read_acl_permissions(list_of_bucket)
                logging.error(list_of_bucket)
                bucket_acl_value = aws_s3_acl.get_bucket_acl(list_of_bucket)

                dict_to_save_csv = display_bucket_to_dict(bucket_acl_value)

                make_csv_with_pandas([dict_to_save_csv], file_name=file_output)
            else:
                dict_to_save_csv = []
                aws_s3_acl.get_acl_list_of_bucket()
                list_of_bucket = aws_s3_acl.list_of_bucket

                for bucket in list_of_bucket:
                    tmp_bucket = display_bucket_to_dict(bucket)
                    dict_to_save_csv.append(tmp_bucket)

                make_csv_with_pandas(dict_to_save_csv, file_name=file_output)

        except NoCredentialsError:
            print(
                "Please make sure that you have a aws credential  config "
                "before use this command "
            )
        except Exception as e:
            logging.error(e)
        except ConnectionError:
            logging.warning("Connection not found")


if __name__ == "__main__":
    main()
