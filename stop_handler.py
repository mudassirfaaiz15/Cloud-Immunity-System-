 Optional Lambda Function – Stops resources without deleting them.

import boto3
import os

def lambda_handler(event, context):
    resource_id = event["queryStringParameters"].get("resourceId")
    resource_type = event["queryStringParameters"].get("type")

    try:
        if resource_type == "EC2 Instance":
            ec2 = boto3.client("ec2")
            ec2.stop_instances(InstanceIds=[resource_id])
        elif resource_type == "RDS Instance":
            rds = boto3.client("rds")
            rds.stop_db_instance(DBInstanceIdentifier=resource_id)
        elif resource_type == "Lambda Function":
            lambda_client = boto3.client("lambda")
            lambda_client.put_function_concurrency(FunctionName=resource_id, ReservedConcurrentExecutions=0)
        else:
            return {'statusCode': 400, 'body': f"Unsupported resource type: {resource_type}"}

        return {
            'statusCode': 200,
            'body': f"✅ {resource_type} ({resource_id}) has been stopped/disabled."
        }

    except Exception as e:
        return {'statusCode': 500, 'body': f"❌ Error: {str(e)}"}
