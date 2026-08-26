# Marketing Campaign Management API

RESTful API quản lý chiến dịch Marketing được xây dựng bằng **FastAPI**, **SQLAlchemy** và **MySQL**.

## 1. Công nghệ sử dụng

- Python 3.10+
- FastAPI
- SQLAlchemy
- MySQL
- PyMySQL
- Pydantic
- JWT
- bcrypt / Passlib
- Uvicorn
- python-dotenv

## 2. Cấu trúc project

```text
campaign_management/
│
├── app/
│   ├── core/
│   │   └── config.py
│   │
│   ├── db/
│   │   ├── seed.py
│   │   └── database.py
│   │
│   ├── dependencies/
│   │   └── auth.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── campaign.py
│   │   ├── campaign_member.py
│   │   ├── campaign_task.py
│   │   └── campaign_audit_log.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── campaign.py
│   │   ├── campaign_member.py
│   │   ├── campaign_task.py
│   │   └── response.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── campaign_service.py
│   │   ├── campaign_member_service.py
│   │   └── campaign_task_service.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── campaign.py
│   │   └── campaign_task.py
│   │
│   ├── utils/
│   │   ├── rate_limit.py
│   │   └── exceptions.py
│   │
│   └── main.py
│
├── .env.example
├── requirements.txt
└── README.md
