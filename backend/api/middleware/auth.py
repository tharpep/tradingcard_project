"""
Authentication middleware for API routes
"""

from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from services.auth_service import auth_service
from config import Config
import logging

logger = logging.getLogger(__name__)

# Security schemes
admin_scheme = HTTPBearer()
user_scheme = HTTPBearer()

class User:
    """User context for authenticated requests"""
    def __init__(self, user_id: str, email: str, username: str):
        self.id = user_id
        self.email = email
        self.username = username

async def verify_admin_api_key(credentials: HTTPAuthorizationCredentials = Depends(admin_scheme)) -> str:
    """
    Verify admin API key for CLI access
    
    Args:
        credentials: Bearer token from request
        
    Returns:
        Admin API key if valid
        
    Raises:
        HTTPException: If API key is invalid
    """
    api_key = credentials.credentials
    
    # For now, we'll use the SUPABASE_KEY as the admin key
    # In production, you'd want a separate admin API key
    if api_key != Config.SUPABASE_KEY:
        logger.warning(f"Invalid admin API key attempt: {api_key[:10]}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.info("Admin API key verified")
    return api_key

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(user_scheme)) -> User:
    """
    Get current user from JWT token
    
    Args:
        credentials: Bearer token from request
        
    Returns:
        User object if token is valid
        
    Raises:
        HTTPException: If token is invalid
    """
    token = credentials.credentials
    
    try:
        # Validate JWT token with auth service
        user_data = auth_service.get_user_from_token(token)
        
        if not user_data or not user_data.get('user'):
            logger.warning("Invalid JWT token provided")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_info = user_data['user']
        profile = user_data.get('profile', {})
        
        user = User(
            user_id=user_info.id,
            email=user_info.email,
            username=profile.get('username', user_info.email)
        )
        
        logger.info(f"User authenticated: {user.username} ({user.email})")
        return user
        
    except Exception as e:
        logger.error(f"Token validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token validation failed",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_optional_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))) -> Optional[User]:
    """
    Get current user from JWT token (optional)
    
    Args:
        credentials: Optional Bearer token from request
        
    Returns:
        User object if token is valid, None if no token provided
    """
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None
