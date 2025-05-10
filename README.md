# PoC Serverless: API Books com AWS SAM

Este projeto demonstra uma arquitetura Serverless utilizando o [AWS SAM (Serverless Application Model)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html), com:

- **ProducerFunction**: API Gateway (POST `/books`) → Lambda → SQS
- **ConsumerFunction**: SQS trigger → Lambda → DynamoDB
- **ListBooksFunction**: API Gateway (GET `/books`) → Lambda → DynamoDB Scan
- **Proteção com API Key**
- **Observabilidade com AWS X-Ray**
- **Frontend**: HTML estático + TailwindCSS

---

## 🧰 O que é o AWS SAM?

O AWS SAM é um framework da AWS para desenvolvimento de aplicações serverless. Ele usa o CLI `sam` para:
- Escrever infraestrutura como código com sintaxe simplificada (`template.yaml`)
- Simular invocações locais
- Empacotar, fazer deploy e monitorar funções Lambda

---

## ⚙️ Pré-requisitos

- Conta AWS com permissões para criar: Lambda, API Gateway, SQS, DynamoDB
- AWS CLI configurado (`aws configure`)
- AWS SAM CLI instalado
- Python 3.9+
- Node.js (opcional para o frontend local)

---

## 🚀 Backend (SAM)

### Clonar repositório

```bash
git clone <repo_url>
cd <repo_folder>
```

### Build e deploy

```bash
rm -rf .aws-sam
sam build --template-file template.yaml
sam deploy --guided --template-file template.yaml
```

Durante o deploy:

- Nome da stack: `unicarioca-202501`
- Região: `us-east-1`
- Permitir criação de IAM Roles
- Habilitar rollback se quiser

**Outputs importantes:**

- `ApiUrl`: URL base da API (ex: https://abc123.execute-api.us-east-1.amazonaws.com/Prod/books)
- `ApiKey`: valor para usar no header `x-api-key`

---

## 🧪 Testes com cURL

### Criar livro (Producer)

```bash
curl -i -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d '{"id":"600","title":"Dom Quixote","author":"Miguel de Cervantes"}'
```

### Listar livros (ListBooks)

```bash
curl -i -X GET "$API_URL" \
  -H "x-api-key: $API_KEY"
```

---

## 🧪 Testes Locais com SAM

### Gerar evento SQS

```bash
sam local generate-event sqs receive-message \
  --body '{"id":"600","title":"Dom Quixote","author":"Miguel de Cervantes"}' > event.json
```

### Executar função Consumer local

```bash
sam local invoke ConsumerFunction -e event.json --env-vars env.json
```

---

## 🎨 Frontend

### Estrutura

```bash
frontend/
├── index.html
├── script.js
├── style.css
├── awslogo.png
├── unicarioca.jpg
├── default-cover.png
```

### Servir localmente

```bash
cd frontend
python3 -m http.server 8000
```

Acesse: [http://localhost:8000](http://localhost:8000)

---

## 📈 Observabilidade

- Todas as funções têm `Tracing: Active`
- Permissão `AWSXRayDaemonWriteAccess` incluída

---

## 🔐 Segurança com API Key

- Criada via `AWS::ApiGateway::ApiKey`
- Associada ao `UsagePlan`
- Obrigatória no método POST e GET

---

## 📦 Extras

- Você pode adicionar upload de imagens com S3
- Criar uma Dead Letter Queue (DLQ)
- Criar alertas com CloudWatch
- Evoluir o frontend com React ou Vue
- Implementar CI/CD com GitHub Actions ou AWS CodePipeline

---

> PoC desenvolvida para alunos da Unicarioca — para fins educacionais