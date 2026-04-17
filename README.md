# Pizza Ordering App - Advanced task

A pizza ordering application built with Flask, SQLite, and a command-line client.

---

## Features

### Customer API
- List menu (`GET /menu`)
- Create order (`POST /order`)
- Check order status (`GET /order/<order_id>`)
- Cancel order if status allows (`DELETE /order/<order_id>`)

### Admin API
- Token-based authentication
- Add pizza to menu (`POST /menu`)
- Delete pizza from menu (`DELETE /menu/<pizza_id>`)
- Force-cancel order (`DELETE /admin/order/<order_id>`)

### CLI
- List menu
- Create order
- Check order status
- Cancel order
- Add pizza (admin)
- Delete pizza (admin)
- Force-cancel order (admin)

### Testing
- Backend API tests with pytest
- Mocked CLI tests with pytest

---

## Tech Stack

- Python
- Flask
- SQLite
- Flasgger (Swagger UI)
- requests
- pytest

---

## Project Structure

```text
3_advanced_task/
├── client/
│   ├── api/
│   ├── commands/
│   ├── cli.py
│   ├── config.py
│   └── requirements.txt
├── server/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── db.py
│   │   └── schema.sql
│   ├── instance/
│   ├── run.py
│   ├── requirements.txt
│   └── .env
├── tests/
│   ├── api/
│   ├── cli/
│   └── conftest.py
└── README.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd 3_advanced_task
```

### 2. Set up the server

```bash
cd server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `server/.env`:

```env
ADMIN_TOKEN=my-secret-token
```

Initialize the database:

```bash
flask --app run.py init-db
```

Run the server:

```bash
python run.py
```

Swagger UI will be available at:

```
http://127.0.0.1:5000/apidocs/
```

### 3. Set up the client

In a new terminal:

```bash
cd client
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## API Endpoints

### Customer

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/menu` | List all pizzas |
| `POST` | `/order` | Create a new order |
| `GET` | `/order/<order_id>` | Check order status |
| `DELETE` | `/order/<order_id>` | Cancel an order |

### Admin

Requires header:

```
Authorization: Bearer <admin-token>
```

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/admin/check` | Verify admin token |
| `POST` | `/menu` | Add pizza to menu |
| `DELETE` | `/menu/<pizza_id>` | Delete pizza from menu |
| `DELETE` | `/admin/order/<order_id>` | Force-cancel an order |

---

## Example API Requests

### Create order

`POST /order`

```json
{
  "customer_name": "Nikola",
  "address": "Novi Sad, Example Street 12",
  "items": [
    { "pizza_id": 1, "quantity": 2 },
    { "pizza_id": 2, "quantity": 1 }
  ]
}
```

### Add pizza as admin

`POST /menu`

Header:

```
Authorization: Bearer my-secret-token
```

Body:

```json
{
  "name": "Quattro Formaggi",
  "price": 12.5,
  "is_available": true
}
```

---

## CLI Usage

Run all commands from the `client/` folder.

### Customer commands

**List menu:**

```bash
python cli.py menu
```

**Create order:**

```bash
python cli.py create-order --customer-name "Nikola" --address "Novi Sad, Example 12" --item 1:2 --item 2:1
```

**Get order:**

```bash
python cli.py get-order --order-id 1
```

**Cancel order:**

```bash
python cli.py cancel-order --order-id 1
```

### Admin commands

**Add pizza:**

```bash
python cli.py add-pizza --token my-secret-token --name "Quattro Formaggi" --price 12.5 --is-available true
```

**Delete pizza:**

```bash
python cli.py delete-pizza --token my-secret-token --pizza-id 5
```

**Force-cancel order:**

```bash
python cli.py admin-cancel-order --token my-secret-token --order-id 2
```

---

## Running Tests

From the project root:

```bash
pytest tests -v
```



---

## Notes

- The database is stored locally as a SQLite file.
- The admin token is loaded from `server/.env`.
- The SQLite database file is not committed to git.
- Swagger UI is included for easier API testing.
