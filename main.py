import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import boto3
from manage import scan_single_bucket, make_a_csv_file
from config import setup_config, setup_credentials, get_region
from scrapping import scrapping


def launch():
    field_head = [
        "Owner_ID",
        "bucket_name",
        'url',
        "private",
        "public-read",
        "public-read-write",
        "aws-exec-read",
        "authenticated-read",
        'log-delivery-write'

    ]
    responses = []
    s3 = boto3.resource('s3')
    buckets = s3.buckets.all()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(scan_single_bucket, bucketName.name, get_region()): bucketName for
            bucketName in buckets
        }
        # modifier
        for future in as_completed(futures):
            responses.append(future.result())
            if future.exception():
                print(f"Bucket scan raised exception: {futures[future]} - {future.exception()}")
    make_a_csv_file(field_head, responses)
    # print("Hello world")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scrap-bucket', dest='bucket_name', help='Scan the bucket, if exist, and provide public properties')

    subparsers = parser.add_subparsers(title='mode', dest='mode')

    # Setup Config Mode
    parser_config = subparsers.add_parser('setup-config', help="Local AWS Configuration of config file")
    parser_config.add_argument('--region', '-r', dest='region', help='Name of the AWS region.', required=True)
    parser_config.add_argument('--output', '-o', dest='output', help='Name of the AWS CLI output format. Default: json',
                               default='json')

    # Setup Credentials Mode
    parser_cred = subparsers.add_parser('setup-cred', help="Local AWS Configuration of credentials file")
    parser_cred.add_argument('--id', '-i', dest='aws_access_key_id', help='Represents the AWS Access Key Id.',
                             required=True)
    parser_cred.add_argument('--key', '-k', dest='aws_secret_access_key', help='Represents the AWS Secret Access Key',
                             required=True)

    # Parse the args
    args = parser.parse_args()

    if args.bucket_name:
        scrapping(args.bucket_name)

    if args.mode == 'setup-config':
        if args.output != 'json':
            setup_config(region=args.region, output=args.output)
        else:
            setup_config(region=args.region)
        print("Configuration of the config file done.")
    elif args.mode == 'setup-cred':
        setup_credentials(id=args.aws_access_key_id, key=args.aws_secret_access_key)
        print("Configuration of the credentials file done.")


if __name__ == '__main__':
    main()
