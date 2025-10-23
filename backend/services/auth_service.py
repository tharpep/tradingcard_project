import logging
from typing import Optional, Dict, Any
from supabase import create_client, Client
from config import Config

logger = logging.getLogger(__name__)

class AuthService:
    """Service for handling Supabase authentication"""
    
    def __init__(self):
        """Initialize Supabase client"""
        try:
            self.supabase: Client = create_client(
                Config.SUPABASE_URL,
                Config.SUPABASE_KEY
            )
            logger.info("AuthService initialized with Supabase client")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            self.supabase = None
    
    def sign_up(self, email: str, password: str, username: str) -> Dict[str, Any]:
        """
        Register a new user
        
        Args:
            email: User's email address
            password: User's password
            username: User's chosen username
            
        Returns:
            Dict containing user data and session info
        """
        logger.info(f"Registering new user: {username} ({email})")
        
        if not self.supabase:
            logger.error("Supabase client not initialized")
            return {"success": False, "error": "Authentication service unavailable"}
        
        try:
            # Register with Supabase Auth
            response = self.supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {"username": username}
                }
            })
            
            if response.user:
                # Create user profile in our users table
                user_profile = {
                    "id": response.user.id,
                    "username": username,
                    "email": email
                }
                
                # Insert into users table
                profile_response = self.supabase.table("users").insert(user_profile).execute()
                
                logger.info(f"User registered successfully: {username}")
                return {
                    "success": True,
                    "user": response.user,
                    "session": response.session,
                    "profile": profile_response.data[0] if profile_response.data else None
                }
            else:
                logger.error("Registration failed: No user returned")
                return {"success": False, "error": "Registration failed"}
                
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return {"success": False, "error": str(e)}
    
    def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        """
        Sign in an existing user
        
        Args:
            email: User's email address
            password: User's password
            
        Returns:
            Dict containing user data and session info
        """
        logger.info(f"Signing in user: {email}")
        
        if not self.supabase:
            logger.error("Supabase client not initialized")
            return {"success": False, "error": "Authentication service unavailable"}
        
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user and response.session:
                # Get user profile from our users table
                profile_response = self.supabase.table("users").select("*").eq("id", response.user.id).execute()
                
                logger.info(f"User signed in successfully: {response.user.email}")
                return {
                    "success": True,
                    "user": response.user,
                    "session": response.session,
                    "profile": profile_response.data[0] if profile_response.data else None
                }
            else:
                logger.error("Sign in failed: No user or session returned")
                return {"success": False, "error": "Sign in failed"}
                
        except Exception as e:
            logger.error(f"Sign in error: {e}")
            return {"success": False, "error": str(e)}
    
    def get_user_from_token(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Get user information from JWT token
        
        Args:
            access_token: JWT access token
            
        Returns:
            User data if token is valid, None otherwise
        """
        try:
            # Set the session with the provided token
            self.supabase.auth.set_session(access_token, "")
            
            # Get user from token
            response = self.supabase.auth.get_user()
            
            if response.user:
                # Get user profile
                profile_response = self.supabase.table("users").select("*").eq("id", response.user.id).execute()
                
                return {
                    "user": response.user,
                    "profile": profile_response.data[0] if profile_response.data else None
                }
            else:
                logger.warning("Invalid token: No user found")
                return None
                
        except Exception as e:
            logger.error(f"Token validation error: {e}")
            return None
    
    def sign_out(self) -> bool:
        """
        Sign out the current user
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.supabase.auth.sign_out()
            logger.info("User signed out successfully")
            return True
        except Exception as e:
            logger.error(f"Sign out error: {e}")
            return False
    
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user profile by ID
        
        Args:
            user_id: User's UUID
            
        Returns:
            User profile data or None
        """
        try:
            response = self.supabase.table("users").select("*").eq("id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error getting user profile: {e}")
            return None
    
    def update_user_profile(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update user profile
        
        Args:
            user_id: User's UUID
            updates: Dictionary of fields to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.supabase.table("users").update(updates).eq("id", user_id).execute()
            logger.info(f"User profile updated: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating user profile: {e}")
            return False
    
    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user (admin function for testing)
        
        Args:
            user_id: User's UUID to delete
            
        Returns:
            True if successful, False otherwise
        """
        if not self.supabase:
            logger.error("Supabase client not initialized")
            return False
            
        try:
            # Delete from users table first
            self.supabase.table("users").delete().eq("id", user_id).execute()
            logger.info(f"User deleted from users table: {user_id}")
            return True
        except Exception as e:
            logger.error(f"User deletion error: {e}")
            return False

# Create global instance
auth_service = AuthService()
