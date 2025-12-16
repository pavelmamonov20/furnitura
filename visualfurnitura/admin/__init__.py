"""
Admin package for VisualFurnitura
Contains all administration-related modules
"""

from .hardware_admin import HardwareAdminDialog
from .profile_admin import ProfileAdminDialog

__all__ = ['HardwareAdminDialog', 'ProfileAdminDialog']