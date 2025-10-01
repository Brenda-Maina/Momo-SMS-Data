# MoMo SMS Transactions API Documentation

Secure REST API for managing SMS transaction data from mobile money services.

## Base URL
http://localhost:8000

## Authentication
This API uses Basic Authentication.

Available Credentials:
- Username: admin, Password: password123
- Username: user, Password: momo2024

## Endpoints

### 1. Get All Transactions
Endpoint & Method: GET /transactions

Request Example:
curl -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" http://localhost:8000/transactions

Response Example:
{
  "count": 20,
  "transactions": [
    {
      "id": 1,
      "address": "MPESA",
      "body": "You sent Ksh 1,000.00 to ALICE KIRUI",
      "date": "1642252800000",
      "type": "1"
    }
  ]
}

### 2. Get Single Transaction
Endpoint & Method: GET /transactions/{id}

Request Example:
curl -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" http://localhost:8000/transactions/1

Response Example:
{
  "id": 1,
  "address": "MPESA",
  "body": "You sent Ksh 1,000.00 to ALICE KIRUI",
  "date": "1642252800000",
  "type": "1"
}

### 3. Create Transaction
Endpoint & Method: POST /transactions

Request Example:
curl -X POST -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" -H "Content-Type: application/json" -d '{"address":"MPESA","body":"New transaction"}' http://localhost:8000/transactions

Response Example:
{
  "message": "Transaction created successfully",
  "id": 21
}

### 4. Update Transaction
Endpoint & Method: PUT /transactions/{id}

Request Example:
curl -X PUT -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" -H "Content-Type: application/json" -d '{"body":"Updated transaction"}' http://localhost:8000/transactions/1

Response Example:
{
  "message": "Transaction updated successfully"
}

### 5. Delete Transaction
Endpoint & Method: DELETE /transactions/{id}

Request Example:
curl -X DELETE -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" http://localhost:8000/transactions/1

Response Example:
{
  "message": "Transaction deleted successfully"
}

## Error Codes
Code	Description
400	Bad Request
401	Unauthorized
404	Not Found
500	Server Error