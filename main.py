"""
    Author: Edmond Ghislain MAKOLLE and Noutcheu Libert
"""
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

import boto3
from botocore.exceptions import NoCredentialsError
from requests.exceptions import HTTPError, RequestException, Timeout

from core.aws.aws_setting import AwsSetting
from core.aws.service import S3Acl, display_bucket_to_dict
from core.business_logic.scrapping import scrapping, scrapping_file
from utils.createcsvfile import makefolder, save_data_to_csv_with_pandas


def parse_config(subparsers) -> None:
    parser_config = subparsers.add_parser(
        "setup-config", help="Local AWS Configuration of config file"
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
        help="Name of the AWS CLI output format. Default: json",
        default="json",
    )


def download_config(subparsers) -> None:
    # Download Mode
    parser_download = subparsers.add_parser(
        "scan",
        help="Create a csv file who  content the buckets information "
        "with acl property",
    )

    parser_download.add_argument(
        "-sf",
        "--scrap-file",
        dest="file",
        help="Scan a file containing a list of buckets name, "
        "and provide public properties. You can "
        "give the name of file if is on the current "
        "directory, of give the path of the file",
    )
    parser_download.add_argument(
        "-s",
        "--scrap-bucket",
        dest="bucket_name",
        help="Scan the bucket, if exist, and provide public properties",
    )
    parser_download.add_argument(
        "-r",
        "--rename",
        dest="rename",
        help="Rename the output file the Default name is rapport_aws_s3.csv",
        required=False,
    )
    parser_download.add_argument(
        "-p",
        "--path",
        dest="download_path",
        help="specify the path of the output file by Default"
        "is << your home folder /ResultsCSV >>",
        required=False,
    )


def parser_credential_config(subparsers) -> None:
    parser_cred = subparsers.add_parser(
        "setup-cred", help="Local AWS Configuration of credentials file"
    )
    parser_cred.add_argument(
        "--id",
        dest="aws_access_key_id",
        help="Represents the AWS Access Key Id.",
        required=True,
    )
    parser_cred.add_argument(
        "--key",
        dest="aws_secret_access_key",
        help="Represents the AWS Secret Access Key",
        required=True,
    )


def args_parser():
    parser = argparse.ArgumentParser(
        description="s3bucket_finder: Analysis of Buckets by AfroCode\n",
        prog="s3bucket_finder",
        allow_abbrev=False,
    )

    subparsers = parser.add_subparsers(title="mode", dest="mode")

    download_config(subparsers)
    # Setup Config Mode
    parse_config(subparsers)
    # Setup Credentials Mode
    parser_credential_config(subparsers)

    # Parse the args
    return parser


def scan_bucket(
    list_of_bucket, aws_s3_acl, file_output, download_path, threads=1
):
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(aws_s3_acl.get_bucket_acl, bucketName): bucketName
            for bucketName in list_of_bucket
        }

        bucket_acl_value = [
            display_bucket_to_dict(future.result())
            for future in as_completed(futures)
        ]

    download_path = save_data_to_csv_with_pandas(
        bucket_acl_value, file_name=file_output, folder_name=download_path
    )

    logging.info("It's over, the file is in the directory %s", download_path)


def launch_aws_scan(
    bucket_name,
    list_of_bucket,
    settings,
    file_output,
    download_path,
    threads=1,
):
    aws_s3_client = boto3.client("s3")
    logging.info("Generation of CSV file with ACL properties...\n")
    aws_s3_acl = S3Acl(list_of_bucket, aws_s3_client, settings)
    if bucket_name is not None:
        scan_bucket(
            [list_of_bucket],
            aws_s3_acl,
            file_output,
            download_path,
            threads=1,
        )

    else:
        scan_bucket(
            list_of_bucket,
            aws_s3_acl,
            file_output,
            download_path,
            threads=threads,
        )


def rename_result(rename_file):
    if rename_file is not None:
        file_output = rename_file
    else:
        file_output = "rapport_aws_s3"

    return file_output


def type_of_bucket_to_scan(args):
    list_of_bucket = []

    if args.bucket_name is not None:
        logging.info(
            f"The bucket scan <{args.bucket_name}> will start in a few "
            f"seconds...\n",
        )
        list_of_bucket = scrapping(args.bucket_name)
        print("\n")  # Just for presentation
    else:
        if args.file is not None:
            logging.info("The file scan will start in a few seconds...\n")
            list_of_bucket = scrapping_file(args.file)
            print("\n")  # Just for presentation

    return list_of_bucket


def check_path_download(download_path):
    try:
        if download_path is not None:
            download_path = download_path
            # check if this folder exist

            if makefolder(download_path) is None:
                raise ValueError(
                    "error with your download path No such directory:  "
                )

            return download_path

    except ValueError:
        logging.error(
            "error with your download path No such directory:  "
            f"{download_path} please check if your parent folder exist"
        )
        exit(0)
    return "ResultsCSV"


def scan(args, settings):
    try:
        download_path: str = check_path_download(args.download_path)
        list_of_bucket = None

        file_output = rename_result(args.rename)
        bucket_name = args.bucket_name
        list_of_bucket = type_of_bucket_to_scan(args)
        launch_aws_scan(
            bucket_name,
            list_of_bucket,
            settings,
            file_output,
            download_path,
            threads=1,
        )

    except NoCredentialsError:
        logging.warning(
            "Please make sure that you have a aws credential config "
            "before use this command."
        )
    except HTTPError:
        logging.error("HTTPError Connection not found")
    except ConnectionError:
        logging.error("Error Connecting:")
    except Timeout:
        logging.error("Timeout Error")
    except RequestException:
        logging.error("Request Connection not found ")


def setup_config(args, settings):
    if args.output != "json":
        settings.config = (args.region, args.output)
    else:
        settings.config = (args.region,)
    logging.info("Configuration of the config file done.")


def setup_credential(args, settings):
    settings.set_credentials(
        access_key=args.aws_access_key_id,
        secret_access_key=args.aws_secret_access_key,
    )
    logging.info("Configuration of the credentials file done.")


def main():
    print("\n")  # Just for presentation
    parser = args_parser()
    args = parser.parse_args()
    settings = AwsSetting()

    if args.mode == "setup-config":
        setup_config(args, settings)
    elif args.mode == "setup-cred":
        setup_credential(args, settings)
    elif args.mode == "scan":
        scan(args, settings)
    else:
        logging.warning("No argument found.\n")
        parser.print_help()


if __name__ == "__main__":
    main()
