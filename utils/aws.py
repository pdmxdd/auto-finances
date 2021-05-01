import boto3

S3 = boto3.resource('s3')

def get_object(bucket_name, object_key):
    return S3.Object(bucket_name, object_key)

def get_bucket(bucket_name):
    bucket = S3.Bucket(bucket_name)
    return bucket

def upload_file_to_bucket(bucket_name, filepath):
    bucket = get_bucket(bucket_name)
    return bucket.upload_file(filepath, filepath.split("/")[-1])

def delete_file_from_bucket(bucket_name, file_key):
    return S3.Object(bucket_name, file_key).delete()