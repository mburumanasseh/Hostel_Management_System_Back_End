"""
Import all database models.

Flask-Migrate uses these imports to detect tables.
"""

from .user import User
from .student import Student
from .block import Block
from .room import Room
from .allocation import Allocation
from .maintenance import MaintenanceRequest
from .payment import Payment

__all__ = [
    "User",
    "Student",
    "Block",
    "Room",
    "Allocation",
    "MaintenanceRequest",
    "Payment",
]