# Data Models Documentation

## User Model

The User model supports multiple roles (Consumer, Farmer, Agribusiness) and both traditional and OAuth-based authentication.

### UserBase (Base Model)
```python
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    full_name: Optional[str] = None
    is_active: bool = True
    role: str = Field(default="consumer")  # consumer, farmer, agribusiness
```

### User (Database Model)
```python
class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    password: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    oauth_provider: Optional[str] = None
    oauth_id: Optional[str] = None
    oauth_data: Optional[Dict[str, Any]] = Field(default=None, sa_type=JSON)
```

## Product Model
```python
class Product(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: str
    price: float
    quantity: int
    image_url: Optional[str] = None
    location: str
    farmer_id: UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## Order Model
```python
class Order(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(foreign_key="product.id")
    customer_id: UUID = Field(foreign_key="user.id")
    farmer_id: UUID = Field(foreign_key="user.id")
    status: str  # pending, paid, delivered, released, cancelled
    total_amount: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Message Model (Firebase)
Chat messages are handled in Firebase for real-time communication. The Message model in the backend is primarily for reference, analytics, or syncing purposes.

```python
class Message(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    sender_id: UUID = Field(foreign_key="user.id")
    receiver_id: UUID = Field(foreign_key="user.id")
    order_id: Optional[UUID] = Field(foreign_key="order.id")
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    firebase_id: Optional[str] = None  # Reference to Firebase message
```

## Real-time Features (Firebase)
- Chat, order status updates, and notifications are managed in Firebase for real-time delivery.
- Backend models may store references or sync data for analytics, reporting, or backup.

## Security & Validation
- Passwords are securely hashed
- Email is unique and validated
- Role-based access enforced
- Data encrypted where necessary

## Migration Strategy
- Alembic for schema migrations
- Version control for all changes
- Safe rollbacks supported

## Field Descriptions

### Base Fields
- `email`: Unique identifier for the user, used for login
- `full_name`: Optional display name for the user
- `is_active`: Boolean flag indicating if the account is active
- `role`: User role for authorization (default: "consumer")

### User-Specific Fields
- `id`: Unique UUID primary key
- `password`: Hashed password (optional for OAuth users)
- `created_at`: Timestamp of account creation
- `updated_at`: Timestamp of last update

### OAuth Fields
- `oauth_provider`: Name of the OAuth provider (e.g., "google", "github")
- `oauth_id`: Unique identifier from the OAuth provider
- `oauth_data`: JSON field storing additional OAuth provider data

## Database Relationships

The User model is designed to be self-contained but can be extended to support:
- User sessions
- User permissions
- User preferences
- Audit logs

## Data Validation

1. **Email Validation**
   - Must be unique
   - Must be a valid email format
   - Indexed for fast lookups

2. **Password Requirements**
   - Hashed before storage
   - Optional for OAuth users
   - Secure storage practices

3. **OAuth Data**
   - Structured JSON storage
   - Provider-specific data
   - Secure token storage

## Model Usage

### Creating a New User
```python
user = User(
    email="user@example.com",
    full_name="John Doe",
    password="hashed_password"
)
```

### OAuth User Creation
```python
oauth_user = User(
    email="user@example.com",
    oauth_provider="google",
    oauth_id="google_123",
    oauth_data={"picture": "url", "locale": "en"}
)
```

## Security Considerations

1. **Password Security**
   - Never store plain text passwords
   - Use secure hashing algorithms
   - Implement password policies

2. **OAuth Security**
   - Secure token storage
   - Provider validation
   - Token refresh handling

3. **Data Protection**
   - Sensitive data encryption
   - Access control
   - Audit logging

## Database Indexes

1. **Primary Index**
   - `id` (UUID)

2. **Secondary Indexes**
   - `email` (unique)
   - `oauth_id` (when using OAuth)

## Migration Strategy

The model uses Alembic for database migrations:
- Version control for schema changes
- Safe database updates
- Data migration support
- Rollback capabilities 