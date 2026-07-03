from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import require_roles

router = APIRouter(prefix="/audit-logs", tags=["Audit Trail"])


@router.get("/", response_model=list[schemas.AuditLogOut])
def list_audit_logs(
    table_name: str | None = None,
    record_id: str | None = None,
    changed_by: str | None = None,
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db),
    _: models.User = Depends(require_roles(models.UserRole.ADMIN)),
):
    """مرور لاگ تغییرات (فقط admin) — ISO/IEC 17025 بند 8.4.

    Browse the audit trail (admin only). Filterable by table, record, and user.
    """
    q = db.query(models.AuditLog).order_by(models.AuditLog.changed_at.desc())
    if table_name:
        q = q.filter(models.AuditLog.table_name == table_name)
    if record_id:
        q = q.filter(models.AuditLog.record_id == record_id)
    if changed_by:
        q = q.filter(models.AuditLog.changed_by == changed_by)
    return q.limit(limit).all()
