from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.user import User
from ..core.dependencies import get_db

def get_current_user(db: Session = Depends(get_db)) -> User:
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user

def get_admin(current_user: User = Depends(get_current_user)) -> User:
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return current_user

def get_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user
