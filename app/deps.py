"""Dependencyهای احراز هویت و کنترل دسترسی مبتنی بر نقش (RBAC).

طبق ISO/IEC 17025 بند 6.2 (صلاحیت و اختیارات پرسنل) و 8.4 (کنترل سوابق):
هویت کاربر همیشه از توکن JWT استخراج می‌شود، نه از بدنهٔ درخواست.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt

from . import models, auth
from .database import get_db
from .i18n import bi

# آدرس گرفتن توکن؛ دکمهٔ Authorize در /docs از همین استفاده می‌کند.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    """توکن را اعتبارسنجی و کاربر فعال را برمی‌گرداند."""
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=bi("توکن نامعتبر یا منقضی است", "Invalid or expired token"),
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth.decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise cred_exc
    except jwt.PyJWTError:
        raise cred_exc

    user = db.get(models.User, user_id)
    if not user or not user.is_active:
        raise cred_exc
    return user


def require_roles(*roles: models.UserRole):
    """Dependency می‌سازد که فقط نقش‌های مجاز را عبور می‌دهد.

    نمونه: ``Depends(require_roles(UserRole.ANALYST, UserRole.ADMIN))``
    """
    def checker(current_user: models.User = Depends(get_current_user)) -> models.User:
        if current_user.role not in roles:
            allowed = ", ".join(r.value for r in roles)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=bi(
                    f"نقش شما ({current_user.role.value}) مجاز نیست؛ نقش‌های مجاز: {allowed}",
                    f"Your role ({current_user.role.value}) is not allowed; allowed roles: {allowed}",
                ),
            )
        return current_user

    return checker
