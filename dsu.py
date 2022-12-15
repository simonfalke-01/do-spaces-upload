import os
import sys
import boto3
import botocore
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    # -e, --endpoint-url
    parser.add_argument('-e', '--endpoint-url', required=True)
    # -r, --region
    parser.add_argument('-r', '--region', required=True)
    # -a, --access-key
    parser.add_argument('-a', '--access-key', required=True)
    # -s, --secret
    parser.add_argument('-s', '--secret', required=True)
    # spaces name
    parser.add_argument('-n', '--spaces-name', required=True)
    # file
    parser.add_argument('file', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    # file name
    parser.add_argument('file_name', nargs='?', type=str, default=sys.stdin)
    args = parser.parse_args()
    return args


def open_file(file):
    with open(file.name, 'r') as f:
        return f.read()


def main():
    args = get_args()

    endpoint_url = args.endpoint_url
    region = args.region
    access_key = args.access_key
    secret = args.secret
    spaces_name = args.spaces_name
    file = args.file
    file_name = args.file_name

    opened = open_file(file)

    session = boto3.session.Session()
    client = session.client('s3',
                            endpoint_url=endpoint_url,
                            config=botocore.config.Config(s3={'addressing_style': 'virtual'}),
                            region_name=region,
                            aws_access_key_id=access_key,
                            aws_secret_access_key=secret
                            )

    client.put_object(Bucket=spaces_name,
                      Key=file_name,
                      Body=opened,
                      ACL='public',
                      Metadata={}
                      )

    print('https://' + spaces_name + '.' + endpoint_url + '/' + file_name)


if __name__ == '__main__':
    main()
