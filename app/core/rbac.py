from typing import Dict, List, Optional, Set
import yaml
from pathlib import Path

from fastapi import HTTPException, status, Depends
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.config.logging import logger


class RBACManager:
    def __init__(self, config_path: Optional[str] = None):
        self.roles: Dict[str, Dict] = {}
        self.permissions: Dict[str, Dict] = {}
        self.wildcard_permission = "*"
        
        if config_path:
            self.load_config(config_path)
        else:
            # Load default config from app/config/roles.yaml
            default_config = Path(__file__).parent.parent / "config" / "roles.yaml"
            self.load_config(str(default_config))

    def load_config(self, config_path: str) -> None:
        """Load roles and permissions from YAML configuration file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                
            if not isinstance(config, dict):
                raise ValueError("Invalid YAML configuration: root must be a dictionary")
                
            self.roles = config.get('roles', {})
            self.permissions = config.get('permissions', {})
            
            # Validate configuration
            self._validate_config()
            
            logger.info(f"Loaded {len(self.roles)} roles and {len(self.permissions)} permissions")
            
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML configuration: {str(e)}")
            raise ValueError(f"Invalid YAML configuration: {str(e)}")
        except Exception as e:
            logger.error(f"Failed to load RBAC configuration: {str(e)}")
            raise ValueError(f"Failed to load RBAC configuration: {str(e)}")

    def _validate_config(self) -> None:
        """Validate the loaded configuration."""
        # Check if roles exist
        if not self.roles:
            logger.warning("No roles defined in configuration")
            
        # Check if permissions exist
        if not self.permissions:
            logger.warning("No permissions defined in configuration")
            
        # Validate each role's permissions
        for role_name, role_data in self.roles.items():
            if not isinstance(role_data, dict):
                raise ValueError(f"Invalid role configuration for '{role_name}': must be a dictionary")
                
            permissions = role_data.get('permissions', [])
            if not isinstance(permissions, list):
                raise ValueError(f"Invalid permissions for role '{role_name}': must be a list")
                
            # Check if permissions exist
            for permission in permissions:
                if permission != self.wildcard_permission and permission not in self.permissions:
                    logger.warning(f"Permission '{permission}' used in role '{role_name}' is not defined")

    def get_role_permissions(self, role: str) -> Set[str]:
        """Get all permissions for a given role."""
        if role not in self.roles:
            raise ValueError(f"Role '{role}' not found")
            
        permissions = set(self.roles[role].get('permissions', []))
        
        # If role has wildcard permission, grant all permissions
        if self.wildcard_permission in permissions:
            return {self.wildcard_permission}
            
        return permissions

    def has_permission(self, role: str, permission: str) -> bool:
        """Check if a role has a specific permission."""
        logger.debug(f"Checking permission '{permission}' for role '{role}'")
        try:
            role_permissions = self.get_role_permissions(role)
            has_permission = (
                self.wildcard_permission in role_permissions or
                permission in role_permissions
            )
            logger.debug(f"Permission check result: {has_permission}")
            return has_permission
        except ValueError:
            return False

    def get_permission_metadata(self, permission: str) -> Optional[Dict]:
        """Get metadata for a specific permission."""
        return self.permissions.get(permission)

    def get_all_roles(self) -> List[str]:
        """Get list of all available roles."""
        return list(self.roles.keys())

    def get_all_permissions(self) -> List[str]:
        """Get list of all available permissions."""
        return list(self.permissions.keys())

    def validate_permission(self, permission: str) -> bool:
        """Validate if a permission exists in the system."""
        return permission in self.permissions or permission == self.wildcard_permission


# Create a singleton instance
rbac_manager = RBACManager()


class PermissionChecker:
    def __init__(self, required_permission: str):
        self.required_permission = required_permission
        logger.debug(f"Initialized PermissionChecker for permission: {required_permission}")

    async def __call__(self, user: User) -> bool:
        """Check if the user's role has the required permission."""
        logger.debug(f"Starting permission check for user: {user.email} with role: {user.role}")
        try:
            logger.debug(f"Checking permission '{self.required_permission}' for role '{user.role}'")
            if not rbac_manager.has_permission(user.role, self.required_permission):
                logger.warning(f"Permission '{self.required_permission}' denied for role '{user.role}'")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission '{self.required_permission}' required"
                )
            logger.debug(f"Permission '{self.required_permission}' granted for role '{user.role}'")
            return True
        except Exception as e:
            logger.error(f"Unexpected error in permission check: {str(e)}")
            raise


def require_permission(permission: str):
    """Decorator to require a specific permission for an endpoint."""
    async def permission_dependency(user: User = Depends(get_current_user)) -> bool:
        logger.debug(f"Checking permission '{permission}' for user: {user.email}")
        if not rbac_manager.has_permission(user.role, permission):
            logger.warning(f"Permission '{permission}' denied for role '{user.role}'")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission}' required"
            )
        logger.debug(f"Permission '{permission}' granted for role '{user.role}'")
        return True
    return permission_dependency 