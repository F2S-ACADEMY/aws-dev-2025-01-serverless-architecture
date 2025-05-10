import os
import json
import boto3

# Cliente SQS
sqs = boto3.client("sqs")
QUEUE_URL = os.environ["SQS_QUEUE_URL"]

def handler(event, context):
    """
    Espera um POST com JSON:
      { "id": "123", "title": "Meu Livro", "author": "Fulano" , "genre": "genero do livro"}
    """
    try:
        body = json.loads(event.get("body", "{}"))
        # Validação simples
        if not all(k in body for k in ("id", "title", "author","genre")):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Campos obrigatórios: id, title, author, genre"})
            }

        # Enfileira a mensagem
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(body)
        )

        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Livro enfileirado com sucesso", "item": body})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }