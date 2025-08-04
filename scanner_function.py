
 Scans resources and sends email report via SES:


import boto3
import json
from datetime import datetime
from collections import defaultdict

# AWS clients
sts = boto3.client('sts')
iam = boto3.client('iam')
ec2 = boto3.client('ec2', region_name='us-east-1')
rds = boto3.client('rds', region_name='us-east-1')
s3 = boto3.client('s3')
lambda_client = boto3.client('lambda')
autoscaling = boto3.client('autoscaling', region_name='us-east-1')
ses = boto3.client('ses')

SENDER = "your-verified-email@example.com"
RECIPIENTS = ["your-verified-email@example.com"]
CHARSET = "UTF-8"
API_GATEWAY_BASE = "https://your-api-id.execute-api.us-east-1.amazonaws.com/prod"
TARGET_REGION = "us-east-1"
ROOT_USER_ID = "root"

def lambda_handler(event, context):
    try:
        account_id = sts.get_caller_identity()['Account']
        now = datetime.utcnow()
        resources = []

        # Scan EC2
        reservations = ec2.describe_instances().get('Reservations', [])
        for res in reservations:
            for inst in res.get('Instances', []):
                state = inst['State']['Name']
                status = 'active' if state == 'running' else 'inactive'
                resources.append({
                    'ResourceType': 'EC2 Instance',
                    'ResourceId': inst['InstanceId'],
                    'Status': status,
                    'Created': inst['LaunchTime'].strftime('%Y-%m-%d'),
                    'Region': TARGET_REGION
                })

        # Scan S3
        buckets = s3.list_buckets().get('Buckets', [])
        for b in buckets:
            resources.append({
                'ResourceType': 'S3 Bucket',
                'ResourceId': b['Name'],
                'Status': 'active',
                'Created': b['CreationDate'].strftime('%Y-%m-%d'),
                'Region': TARGET_REGION
            })

        # Scan RDS
        dbs = rds.describe_db_instances().get('DBInstances', [])
        for db in dbs:
            status = 'active' if db['DBInstanceStatus'] == 'available' else 'inactive'
            resources.append({
                'ResourceType': 'RDS Instance',
                'ResourceId': db['DBInstanceIdentifier'],
                'Status': status,
                'Created': db['InstanceCreateTime'].strftime('%Y-%m-%d'),
                'Region': TARGET_REGION
            })

        # Scan Lambda
        functions = lambda_client.list_functions().get('Functions', [])
        for fn in functions:
            resources.append({
                'ResourceType': 'Lambda Function',
                'ResourceId': fn['FunctionName'],
                'Status': 'active',
                'Created': fn['LastModified'],
                'Region': 'global'
            })

        # Generate HTML email
        html_rows = ""
        for r in resources:
            html_rows += f"""
            <tr>
                <td>{r['ResourceType']}</td>
                <td>{r['ResourceId']}</td>
                <td>{r['Status']}</td>
                <td>{r['Created']}</td>
                <td><a href='{API_GATEWAY_BASE}/stop?resourceId={r["ResourceId"]}&type={r["ResourceType"]}'>Stop</a> |
                    <a href='{API_GATEWAY_BASE}/delete?resourceId={r["ResourceId"]}&type={r["ResourceType"]}'>Delete</a></td>
            </tr>"""

        html_body = f"""
        <html>
        <body>
            <h2>AWS Resource Report</h2>
            <table border="1">
                <tr><th>Resource Type</th><th>Resource ID</th><th>Status</th><th>Created</th><th>Actions</th></tr>
                {html_rows}
            </table>
        </body>
        </html>"""

        ses.send_email(
            Source=SENDER,
            Destination={'ToAddresses': RECIPIENTS},
            Message={
                'Subject': {'Data': 'Cloud Immunity Report', 'Charset': CHARSET},
                'Body': {'Html': {'Data': html_body, 'Charset': CHARSET}}
            }
        )

        return {'statusCode': 200, 'body': 'Email sent.'}
    except Exception as e:
        return {'statusCode': 500, 'body': f'Error: {str(e)}'}
