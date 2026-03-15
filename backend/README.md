# Project Management & Paid Task Platform - Backend

This is the backend API for the Project Management & Paid Task Platform, built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

## 🚀 Features

- **Auth & RBAC**: Secure authentication using JWT with three distinct roles:
  - **Buyer**: Can create projects and tasks, assign developers, and pay for solutions.
  - **Developer**: Can view assigned tasks and submit solutions (ZIP files).
  - **Admin**: Full access to platform statistics, management of all users, and projects.
- **Task Workflow**: Secure task lifecycle from 'Todo' to 'Submitted' and 'Paid'.
- **File Management**: Secure handling of solution uploads (ZIP files).
- **Security**: Solution downloads are locked until the buyer completes the payment.
- **Admin Dashboard**: Comprehensive stats including user breakdowns, task status, and financial summaries.

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Authentication**: JWT (python-jose) & Passlib (bcrypt)
- **Validation**: [Pydantic](https://pdocs.io/pydantic/)

## 📦 Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd backend
```

### 2. Set up virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Database
Ensure you have a PostgreSQL database running. Update the `DATABASE_URL` in `app/database.py` with your credentials:
```python
DATABASE_URL = "postgresql://user:password@localhost/task_platform"
```

## 🏃 Running the Application

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

- **Interactive API Docs**: `http://localhost:8000/docs`
- **Alternative API Docs**: `http://localhost:8000/redoc`

## 📂 Project Structure

```text
backend/
├── app/
│   ├── routers/       # API endpoints (users, projects, tasks, admin, payment)
│   ├── auth.py        # JWT and hashing logic
│   ├── database.py    # DB engine and session setup
│   ├── deps.py        # Dependencies (Auth guards)
│   ├── main.py        # FastAPI app initialization
│   ├── models.py      # SQLAlchemy models
│   └── schemas.py     # Pydantic validation schemas
├── uploads/           # Storage for submitted task solutions
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## 🔐 API Roles & Permissions

| Endpoint | Method | Permission | Description |
| :--- | :--- | :--- | :--- |
| `/register` | POST | Public | Create a new user account |
| `/login` | POST | Public | Authenticate and get JWT token |
| `/projects` | POST | Buyer | Create a new project |
| `/tasks` | POST | Buyer | Create a task and assign a developer |
| `/tasks/my-tasks` | GET | Developer | View assigned tasks |
| `/admin/stats` | GET | Admin | Access platform analytics |
| `/admin/all-users`| GET | Admin/Buyer | List users (Buyers see only Developers) |

## 📝 License

This project is licensed under the MIT License.
