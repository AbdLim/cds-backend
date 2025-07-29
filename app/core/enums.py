from enum import Enum

class OrderStatus(str, Enum):
    """
    Order status enum defining all possible states and their transitions.
    
    Flow:
    PENDING -> PAID -> DELIVERED -> RELEASED
    Any state -> CANCELLED
    """
    PENDING = "pending"  # Initial state when order is created
    PAID = "paid"  # Customer has paid for the order
    DELIVERED = "delivered"  # Farmer has delivered the product
    RELEASED = "released"  # Payment has been released to farmer
    CANCELLED = "cancelled"  # Order has been cancelled (can happen at any state)

    @classmethod
    def get_valid_transitions(cls, current_status: str) -> list[str]:
        transitions = {
            cls.PENDING: [cls.PAID, cls.CANCELLED],
            cls.PAID: [cls.DELIVERED, cls.CANCELLED],
            cls.DELIVERED: [cls.RELEASED, cls.CANCELLED],
            cls.RELEASED: [],
            cls.CANCELLED: [],
        }
        return transitions.get(cls(current_status), [])

    @classmethod
    def is_valid_transition(cls, current_status: str, new_status: str) -> bool:
        return cls(new_status) in cls.get_valid_transitions(current_status) 