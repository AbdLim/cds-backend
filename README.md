# CDS Attendance -

A modern agricultural trading platform API built with FastAPI, featuring secure authentication, role-based access control (RBAC), and comprehensive trading features.

## 🌟 Features

-   **Authentication & Authorization**

    -   JWT-based authentication
    -   Access and refresh tokens
    -   Secure password hashing
    -   Token refresh mechanism
    -   Role-Based Access Control (RBAC)

-   **User Management**

    -   User registration and login
    -   Profile management
    -   User status control (active/inactive)
    -   Role management

-   **Trading Features**
    -   Product listings
    -   Order management
    -   Transaction tracking
    -   Market analytics

## 🚀 Getting Started

### Prerequisites

-   Python 3.8+
-   Poetry (for dependency management)
-   PostgreSQL
-   Redis

### Installation

1. Clone the repository:

```bash
git clone https://github.com/abdlim/agrotrade.git
cd agrotrade
```

2. Install dependencies:

```bash
poetry install
```

3. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:

```bash
poetry run start
```

## 📦 Database Setup

### Initial Migration

1. Run the initial migration to set up the database schema:

```bash
alembic upgrade head
```

This will create the following tables:

-   `users`: Stores user information and roles
-   `refresh_tokens`: Manages JWT refresh tokens
-   `user_sessions`: Handles user session management

### Managing Migrations

-   Create a new migration:

```bash
alembic revision --autogenerate -m "Description of changes"
```

-   Apply pending migrations:

```bash
alembic upgrade head
```

-   Rollback last migration:

```bash
alembic downgrade -1
```

-   View migration history:

```bash
alembic history
```

-   Check current migration version:

```bash
alembic current
```

## 📚 Architecture

### Core Components

1. **Authentication System**

    - JWT token generation and validation
    - Password hashing and verification
    - Token refresh mechanism

2. **Role-Based Access Control**

    - YAML configuration for roles and permissions
    - Permission checking middleware
    - Role management system

3. **User Management**
    - User model with role support
    - User repository for database operations
    - User service for business logic

### Directory Structure

```
app/
├── config/
│   ├── database.py
│   └── roles.yaml      # RBAC configuration
├── core/
│   └── rbac.py         # RBAC implementation
├── dependencies/
│   └── auth.py         # Auth dependencies
├── models/
│   └── user.py         # User model
├── repositories/
│   ├── base.py         # Base repository
│   └── user.py         # User repository
├── routers/
│   ├── auth.py         # Auth endpoints
│   └── users.py        # User endpoints
├── schemas/
│   ├── auth.py         # Auth schemas
│   └── user.py         # User schemas
└── services/
    ├── auth.py         # Auth service
    └── users.py        # User service
```

## 🔐 Role-Based Access Control

### Configuration

Roles and permissions are defined in `app/config/roles.yaml`:

```yaml
roles:
    user:
        description: "Basic user with standard access"
        permissions:
            - "read:own_profile"
            - "update:own_profile"
            - "read:own_data"

    trader:
        description: "User with trading capabilities"
        permissions:
            - "read:own_profile"
            - "update:own_profile"
            - "create:listing"
            - "update:own_listing"
            - "delete:own_listing"

    admin:
        description: "System administrator with full access"
        permissions:
            - "*" # Wildcard permission grants all access
```

### Using RBAC

1. **Protect Endpoints**

```python
from app.core.rbac import require_permission

@router.get("/users")
async def list_users(
    _: bool = Depends(require_permission("read:all_profiles"))
):
    # Only users with read:all_profiles permission can access
    pass
```

2. **Check Permissions in Code**

```python
from app.core.rbac import rbac_manager

if rbac_manager.has_permission(user.role, "update:user_status"):
    # Do something
    pass
```

## 🔒 Security Considerations

1. **Token Security**

    - Tokens are signed with a secret key
    - Access tokens have short expiration
    - Refresh tokens can be revoked

2. **Password Security**

    - Passwords are hashed using bcrypt
    - Password complexity requirements
    - Rate limiting on login attempts

3. **RBAC Security**
    - Permission checks at endpoint level
    - Role validation
    - Scope-based permissions

## 🧪 Testing

Run tests with:

```bash
poetry run pytest
```

## 📝 API Documentation

Access the API documentation at:

-   Swagger UI: `http://localhost:8000/docs`
-   ReDoc: `http://localhost:8000/redoc`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
