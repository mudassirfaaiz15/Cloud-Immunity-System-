Lambda Function 2 – Validates password before deletion.

import os

HTML_FORM = """
<html>
  <body>
    <h2>Confirm Deletion</h2>
    <form action="/prod/delete" method="post">
      <input type="hidden" name="resourceId" value="{resourceId}">
      <input type="hidden" name="type" value="{resourceType}">
      <label>Password:</label>
      <input type="password" name="password" required />
      <button type="submit">Confirm Delete</button>
    </form>
  </body>
</html>
"""

def lambda_handler(event, context):
    resource_id = event["queryStringParameters"].get("resourceId")
    resource_type = event["queryStringParameters"].get("type")

    body = HTML_FORM.format(resourceId=resource_id, resourceType=resource_type)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html'},
        'body': body
    }
