import argparse

from models.aws_setting import AwsSetting
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

    if args.bucket_name:
        scrapping(args.bucket_name)

    if args.file:
        scrapping_buckets(args.file)

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


if __name__ == '__main__':
    main()
