# SplitWise Clone

A simple expense-sharing application inspired by Splitwise. This project allows users to create groups, add expenses, and automatically calculate how much each member owes or is owed.

## Features
- User and group management
- Add expenses to groups
- Support for equal and percentage-based splits
- Track balances between users
- RESTful API using FastAPI

## Tech Stack
- Python 3
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL (or SQLite for development)
- Alembic (for migrations)

## Database Schema Diagram

```mermaid
erDiagram
    User {
        int id PK
        string name
    }
    Group {
        int id PK
        string name
    }
    GroupMember {
        int id PK
        int group_id FK
        int user_id FK
    }
    Expense {
        int id PK
        string description
        float amount
        int paid_by FK
        enum split_type
        int group_id FK
    }
    ExpenseSplit {
        int id PK
        int expense_id FK
        int user_id FK
        float amount
    }

    User ||--o{ GroupMember : "has"
    Group ||--o{ GroupMember : "has"
    Group ||--o{ Expense : "has"
    Expense ||--o{ ExpenseSplit : "has"
    User ||--o{ Expense : "pays"
    User ||--o{ ExpenseSplit : "owes"
    Expense o{--|| Group : "belongs to"
    GroupMember o{--|| User : "is"
    GroupMember o{--|| Group : "is"
    ExpenseSplit o{--|| Expense : "is part of"
    ExpenseSplit o{--|| User : "is for"
```

## Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL (or SQLite for development)

### Setup
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd SplitWiseClone
   ```
2. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables:**
   - Create a `.env` file in the root directory:
     ```env
     DATABASE_URL=postgresql://user:password@localhost:5432/splitwise_db
     ```
     Or for SQLite (for testing):
     ```env
     DATABASE_URL=sqlite:///./test.db
     ```

5. **Run database migrations (optional):**
   ```bash
   alembic upgrade head
   ```
   Or let SQLAlchemy create tables automatically on first run.

### Running the App
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### API Overview
- `GET /` — Health check
- `POST /groups/` — Create a group
- `POST /groups/{group_id}/members/{user_id}` — Add a user to a group
- `DELETE /groups/{group_id}/members/{user_id}` — Remove a user from a group (only if their balance is zero)
- `POST /expenses/` — Add an expense
- `GET /balances/` — Get balances

**Note:**
- A user can only be removed from a group if their balance in that group is zero (they neither owe nor are owed money).

Explore the full API docs and test endpoints interactively using **Swagger UI** at `http://127.0.0.1:8000/docs` (or `/docs` on your deployment).

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](LICENSE) 