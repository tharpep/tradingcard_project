"""
Authentication routes for frontend
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from services.auth_service import auth_service
from api.middleware.auth import get_current_user, User
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])

# Request/Response models
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    username: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    username: str

class AuthResponse(BaseModel):
    success: bool
    user: UserResponse
    access_token: str
    refresh_token: str

@router.post("/signup", response_model=AuthResponse)
async def signup(user_data: SignupRequest):
    """Register a new user"""
    try:
        logger.info(f"User signup attempt: {user_data.email}")
        
        result = auth_service.sign_up(
            email=user_data.email,
            password=user_data.password,
            username=user_data.username
        )
        
        if not result.get('success'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get('error', 'Registration failed')
            )
        
        user = result['user']
        session = result['session']
        profile = result.get('profile', {})
        
        return AuthResponse(
            success=True,
            user=UserResponse(
                id=user.id,
                email=user.email,
                username=profile.get('username', user.email)
            ),
            access_token=session.access_token,
            refresh_token=session.refresh_token
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signup error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@router.post("/signin", response_model=AuthResponse)
async def signin(credentials: LoginRequest):
    """Sign in an existing user"""
    try:
        logger.info(f"User signin attempt: {credentials.email}")
        
        result = auth_service.sign_in(
            email=credentials.email,
            password=credentials.password
        )
        
        if not result.get('success'):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=result.get('error', 'Invalid credentials')
            )
        
        user = result['user']
        session = result['session']
        profile = result.get('profile', {})
        
        return AuthResponse(
            success=True,
            user=UserResponse(
                id=user.id,
                email=user.email,
                username=profile.get('username', user.email)
            ),
            access_token=session.access_token,
            refresh_token=session.refresh_token
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signin error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sign in failed"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = get_current_user):
    """Get current user information"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username
    )

@router.post("/signout")
async def signout(current_user: User = get_current_user):
    """Sign out the current user"""
    try:
        success = auth_service.sign_out()
        if success:
            return {"message": "Signed out successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Sign out failed"
            )
    except Exception as e:
        logger.error(f"Signout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sign out failed"
        )
