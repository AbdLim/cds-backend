# Architecture Documentation

## System Architecture

Agrotrade follows a clean, layered architecture pattern with clear separation of concerns, tailored for a P2P marketplace with blockchain integration and real-time features via Firebase:

```
┌────────────────────┐
│    API Layer       │  FastAPI Routers
└─────────┬──────────┘
          │
┌─────────▼──────────┐
│  Service Layer     │  Business Logic (Marketplace, Orders, Payments)
└─────────┬──────────┘
          │
┌─────────▼──────────┐
│ Repository Layer   │  Data Access
└─────────┬──────────┘
          │
┌─────────▼──────────┐
│  Database Layer    │  SQLModel/SQLAlchemy
└─────────┬──────────┘
          │
┌─────────▼──────────┐
│  Firebase Layer    │  Real-time chat, order status, notifications
└────────────────────┘
```

## Component Details

### 1. API Layer (Routers)
- Handles HTTP requests and responses
- Input validation using Pydantic schemas
- Route definitions and endpoint handlers
- Authentication middleware
- Error handling and response formatting

### 2. Service Layer
- Implements business logic for:
  - User authentication and role management
  - Product listings and filtering
  - Order and cart management
  - Escrow payment and blockchain integration
  - In-app messaging and notifications (integrates with Firebase)
- Coordinates between repositories and Firebase

### 3. Repository Layer
- Abstracts database operations
- Implements CRUD operations for users, products, orders, and messages
- Handles data persistence and transactions

### 4. Database Layer
- SQLModel models for all entities
- Database migrations with Alembic
- Connection pooling and management
- Query optimization

### 5. Firebase Layer
- Real-time chat between users
- Real-time order status updates
- Real-time notifications
- Syncs with backend for consistency

## Marketplace & Transaction Flow

1. **User Authentication & Role Assignment**
   - Multi-role (Consumer, Farmer, Agribusiness)
   - JWT/OAuth authentication

2. **Product Listing & Discovery**
   - Farmers list products
   - Consumers filter and browse

3. **Order Placement & Escrow Payment**
   - Customer places order, payment held in escrow (blockchain)
   - Order status tracked (real-time updates via Firebase)

4. **Delivery & Fund Release**
   - Upon delivery confirmation, funds released to farmer

5. **In-app Communication**
   - Messaging between buyer and seller (via Firebase)
   - Order notifications (via Firebase)

## Security Architecture

- JWT token-based authentication
- OAuth 2.0 integration
- Password hashing
- Role-based access control (RBAC)
- CORS protection
- Rate limiting
- Data encryption

## Error Handling

- Standardized error responses
- Detailed error logging
- Graceful error recovery
- Client-friendly error messages

## Logging and Monitoring

- Structured logging
- Request/Response logging
- Error tracking
- Performance monitoring
- Audit logging for security events 