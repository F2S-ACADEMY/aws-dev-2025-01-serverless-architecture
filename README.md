PoC Serverless: API Books com AWS SAM

Este repositório apresenta uma prova de conceito (PoC) de uma arquitetura Serverless usando AWS SAM (Serverless Application Model), que permite definir APIs, funções Lambda, filas SQS e tabelas DynamoDB como código, além de rodar e testar localmente.

O que é o AWS SAM?

O AWS SAM é um framework open-source para construir aplicações serverless na AWS. Ele se baseia em CloudFormation e adiciona abstrações simples como AWS::Serverless::Function, AWS::Serverless::Api e templates de políticas. Com o SAM CLI, você pode:

build: empacotar suas Lambdas e templates

local invoke: simular invocações de funções

local start-api: rodar o API Gateway e Lambdas localmente

deploy: criar/update sua stack no AWS CloudFormation

Pré-requisitos

Conta AWS com permissões para criar Lambda, API Gateway, SQS e DynamoDB

AWS CLI instalado e configurado (aws configure)

AWS SAM CLI instalado

Python 3.9+

Node.js (opcional, para evoluir o front-end)

1. Backend (AWS SAM)

git clone <repo_url>
cd <repo_folder>

O arquivo template.yaml contém:

BooksApi (AWS::Serverless::Api) com CORS e proteção por API Key

ProducerFunction (POST /books → SQS)

ListBooksFunction (GET /books → DynamoDB Scan)

ConsumerFunction (SQS trigger → DynamoDB PutItem)

Usage Plan, ApiKey, enlaces de Key ↔ UsagePlan

X-Ray habilitado globalmente para tracing

Build & Deploy no AWS

rm -rf .aws-sam
sam build --template-file template.yaml
sam deploy --guided --template-file template.yaml

Stack Name: unicarioca-202501

Region: us-east-1

Permita criação de IAM Roles

Habilite rollback conforme necessidade

Anote os Outputs:

ApiUrl: endpoint REST (ex: https://.../Prod/books)

ApiKey: valor secreto a usar no header x-api-key

2. Testes via cURL

Inserir um livro (Producer)

curl -i -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d '{"id":"600","title":"Dom Quixote","author":"Miguel de Cervantes"}'

Listar todos os livros (ListBooks)

curl -i -X GET "$API_URL" \
  -H "x-api-key: $API_KEY"

3. Testes Locais com SAM CLI

Para não subir tudo na AWS, você pode simular localmente:

Gerar eventos de SQS

sam local generate-event sqs receive-message \
  --body '{"id":"600","title":"Dom Quixote","author":"Miguel de Cervantes"}' \
  > event.json

Invoke da ConsumerFunction

sam build --template-file template.yaml
sam local invoke ConsumerFunction -e event.json

Start API Gateway local

sam build --template-file template.yaml
sam local start-api --template-file template.yaml --env-vars env.json

env.json deve conter as variáveis de ambiente para a função Producer:

{
  "ProducerFunction": {
    "SQS_QUEUE_URL": "https://sqs.us-east-1.amazonaws.com/636078031479/f2s-academy-books-queue-dev"
  }
}

Testar endpoints localmente

curl -i -X POST http://127.0.0.1:3000/books \
  -H "Content-Type: application/json" \
  -d '{"id":"601","title":"Teste Local","author":"Você"}'

Esses comandos permitem validar seus Lambdas, SQS e API Gateway sem precisar fazer deploy.

4. Frontend estático

cd frontend
# certifique-se de ter os assets: unicarioca.jpg, awslogo.png, default-cover.png
python3 -m http.server 8000

Acesse http://localhost:8000 para ver a lista de livros com design responsivo usando Tailwind CSS.

5. Observabilidade & Autenticação

X-Ray: Tracing: Active em todas as funções + policy AWSXRayDaemonWriteAccess

API Key: uso de UsagePlan e ApiKey para proteger métodos

Próximos passos sugeridos

Adicionar Dead-Letter Queue (DLQ) para o Consumer

Configurar CloudWatch Alarms para erros e tamanho da fila

Criar CI/CD (GitHub Actions ou AWS CodePipeline)

Evoluir front-end para React ou outro framework

Incluir upload de capas no S3 e gravar imageUrl no DynamoDB

PoC desenvolvida para alunos da Unicarioca. Aproveite e explore!