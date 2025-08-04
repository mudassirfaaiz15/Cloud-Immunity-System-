Lambda Function 3 – Performs delete action after password is verified.

import boto3
import os
from urllib.parse import parse_qs

DELETE_PASSWORD = os.environ.get("DELETE_PASSWORD", "admin123")

def lambda_handler(event, context):
    if event.get("headers", {}).get("Content-Type", "") == "application/x-www-form-urlencoded":
        body = parse_qs(event.get("body", ""))
        password = body.get("password", [""])[0]
        resource_id = body.get("resourceId", [""])[0]
        resource_type = body.get("type", [""])[0]
    else:
        return {'statusCode': 400, 'body': 'Invalid content-type'}

    if password != DELETE_PASSWORD:
        return {
            'statusCode': 403,
            'body': "<h3>Incorrect password. <a href='javascript:history.back()'>Try again</a></h3>",
            'headers': {'Content-Type': 'text/html'}
        }

    try:
        if resource_type == "EC2 Instance":
            ec2 = boto3.client("ec2")
            ec2.terminate_instances(InstanceIds=[resource_id])

        elif resource_type == "RDS Instance":
            rds = boto3.client("rds")
            rds.delete_db_instance(DBInstanceIdentifier=resource_id, SkipFinalSnapshot=True)

        elif resource_type == "S3 Bucket":
            s3 = boto3.resource("s3")
            bucket = s3.Bucket(resource_id)
            bucket.objects.all().delete()
            bucket.object_versions.all().delete()
            bucket.delete()

        elif resource_type == "Lambda Function":
            lambda_client = boto3.client("lambda")
            lambda_client.delete_function(FunctionName=resource_id)

        return {
            'statusCode': 200,
            'body': f"<h3>✅ {resource_type} ({resource_id}) deleted successfully.</h3>",
            'headers': {'Content-Type': 'text/html'}
        }

    except Exception as e:
        return {'statusCode': 500, 'body': f"<h3>❌ Error: {str(e)}</h3>", 'headers': {'Content-Type': 'text/html'}}
