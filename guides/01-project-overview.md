# Agrotrade Project Overview

Agrotrade is a P2P on-chain marketplace that connects farmers and cooperatives directly with consumers, enabling the exchange of agricultural products and byproducts.

## Project Structure

```
agrotrade/
├── app/                   # Main application directory
│   ├── config/           # Configuration files
│   ├── core/            # Core functionality
│   ├── db/              # Database related code
│   ├── dependencies/    # FastAPI dependencies
│   ├── models/          # SQLModel database models
│   ├── repositories/    # Data access layer
│   ├── routers/         # API endpoints
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   └── utils/           # Utility functions
├── alembic/             # Database migrations
├── tests/               # Test suite
└── logs/                # Application logs
```

## Technology Stack

- **Framework**: FastAPI
- **Database**: SQLModel (SQLAlchemy + Pydantic)
- **Authentication**: JWT + OAuth
- **API Documentation**: OpenAPI (Swagger) + ReDoc
- **Database Migrations**: Alembic
- **Containerization**: Docker
- **Blockchain Integration**: Web3.py
- **Payment Processing**: Escrow smart contracts
- **Real-time Features**: Firebase (chat, order status, notifications)

## Key Features

1. User Management
   - Multi-role authentication (Consumer, Farmer, Agribusiness)
   - Profile management
   - Role-based dashboards

2. Marketplace
   - Product listings with images
   - Advanced filtering (location, price, quantity)
   - Cart functionality
   - Order management

3. Transaction System
   - Escrow-based payments
   - Smart contract integration
   - Payment gateway integration
   - Order status tracking (with real-time updates via Firebase)

4. Communication
   - In-app messaging system (powered by Firebase)
   - Order notifications (real-time via Firebase)
   - Status updates

5. Security
   - Secure authentication
   - Role-based access control
   - Transaction security
   - Data encryption

## Getting Started

1. Clone the repository
2. Install dependencies using Poetry
3. Set up environment variables
4. Run database migrations
5. Start the application

For detailed setup instructions, see the [Setup Guide](02-setup-guide.md). 