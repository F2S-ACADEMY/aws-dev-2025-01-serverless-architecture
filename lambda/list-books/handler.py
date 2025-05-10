import os, json, boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMO_TABLE"])

def list_books(event, context):
    try:
        items = table.scan().get("Items", [])
        return {
            "statusCode": 200,
            "headers": {
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "*" 
            },
            "body": json.dumps(items)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "*" 
            },
            "body": json.dumps({"error": str(e)})
        }