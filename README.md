# Campaign Management API

Backend API quản lý chiến dịch marketing được xây dựng bằng FastAPI, SQLAlchemy và MySQL.

## Công nghệ

- Python
- FastAPI
- SQLAlchemy
- MySQL
- Pydantic
- JWT
- bcrypt

## Cấu trúc

```text
campaign_management/
|--app/
│   |-- main.py
│   |-- core/
│   |-- db/
│   |-- models/
│   |--schemas/
│   |-- routers/
│   |-- services/
│   |-- dependencies/
│   └── utils/
|-- tests/
|--.env
|-- .env.example
|-- .gitignore
|-- requirements.txt
|-- README.md