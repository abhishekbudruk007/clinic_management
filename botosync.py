# import boto
# import boto.s3
# import sys
# from boto.s3.key import Key

# AWS_ACCESS_KEY_ID = 'AKIA5R5UV6XBCFXPRLXT'
# AWS_SECRET_ACCESS_KEY = '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'

# bucket_name = 'clinicbucket2022'
# conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
#
# #
# # bucket = conn.create_bucket(bucket_name,
# #     location=boto.s3.connection.Location.DEFAULT)
#
#
# bucket =
#
# testfile = "db.sqlite3"
# print("Uploading {} to Amazon S3 bucket {}".format(testfile, bucket_name))
#
# def percent_cb(complete, total):
#     sys.stdout.write('.')
#     sys.stdout.flush()
#
#
# k = Key(bucket)
# k.key = 'db.sqlite3'
# k.set_contents_from_filename(testfile, cb=percent_cb, num_cb=10)
#
#

import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'AKIA5R5UV6XBCFXPRLXT'
SECRET_KEY = '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'


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


uploaded = upload_to_aws('db.sqlite3', 'clinicbucket2022', 'db.sqlite3')