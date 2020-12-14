import json
import boto3
from io import BytesIO
import zipfile

def lambda_handler(event, context):
    s3_resource = boto3.resource('s3')
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    target_bucket = source_bucket
    key_file = event['Records'][0]['s3']['object']['key']

    my_bucket = s3_resource.Bucket(source_bucket)

    zip_obj = s3_resource.Object(bucket_name=source_bucket, key=key_file)
    buffer = BytesIO(zip_obj.get()["Body"].read())
    z = zipfile.ZipFile(buffer)
    for filename in z.namelist():
        file_info = z.getinfo(filename)
        try:
            response = s3_resource.meta.client.upload_fileobj(
                z.open(filename),
                Bucket=target_bucket,
                Key=f'{filename}'
            )
        except Exception as e:
            print(e)
