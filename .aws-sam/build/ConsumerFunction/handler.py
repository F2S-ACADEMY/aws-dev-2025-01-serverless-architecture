import os
import json
import boto3

# Cliente DynamoDB
dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ["DYNAMO_TABLE"]

def handler(event, context):
    """
    Trigger by SQS. Para cada record, faz PutItem no DynamoDB.
    """
    table = dynamodb.Table(TABLE_NAME)

    for record in event.get("Records", []):
        try:
            item = json.loads(record["body"])
            # Exemplo: espera id, title, author
            table.put_item(Item=item)
        except Exception as e:
            # Aqui você pode implementar lógica de dead-letter ou retry
            print(f"Erro ao processar record: {e}", record)

    return {"statusCode": 200, "body": "Processed {} records".format(len(event.get("Records", [])))}
