import sys
import os
import datetime
import boto
import tarfile
from boto.s3.key import Key
from AWS_ACCESS import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,BUCKET_NAME
from config import sender,receivers,EMAIL_HOST,USERNAME,PASSWORD,BARMAN_SOURCE


def download(filename, bucket_name=BUCKET_NAME):
    
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(bucket_name)
    key = Key(bucket, filename)
    headers = {}
    mode = 'wb'
    updating = False
    try:
        with open(filename, mode) as f:
            key.get_contents_to_file(f)
            f.truncate()
        with tarfile.open(filename, "r") as z:
            z.extractall(BARMAN_SOURCE)
            z.close()
        print "Check extracted file at ", BARMAN_SOURCE
        print "Barman restore from S# server. Now use resore script for DB restore"
    except boto.exception.S3ResponseError as e:
        print "Exception ocuured with boto process ",e
        return e.status
    return 200

if len(sys.argv) <= 1:
    print "=================Pass S3 file name as argument==========================="
else:
    download(sys.argv[1])

