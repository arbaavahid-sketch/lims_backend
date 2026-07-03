"""ثبت خودکار لاگ تغییرات (Audit Trail) — ISO/IEC 17025 بند 8.4.

با گوش‌دادن به رویداد ``after_flush`` سشن SQLAlchemy، هر ایجاد/ویرایش/حذف
روی همهٔ جداول (به‌جز خود audit_logs) به‌صورت خودکار ثبت می‌شود:
چه کسی (از ``session.info["user_id"]`` که در احراز هویت ست می‌شود)،
چه زمانی، مقدار قبلی و مقدار جدید (JSON).

نکته: در ``after_flush`` هنوز لیست‌های new/dirty/deleted و تاریخچهٔ
اتریبیوت‌ها در دسترس‌اند و کلیدهای اصلی رکوردهای جدید مقداردهی شده‌اند.
"""
import json
from datetime import datetime

from sqlalchemy import event, inspect

from .database import SessionLocal
from . import models

# جداولی که لاگ نمی‌شوند (جلوگیری از حلقهٔ بی‌نهایت)
_EXCLUDE_TABLES = {"audit_logs"}
# فیلدهای حساس که هرگز در لاگ ذخیره نمی‌شوند
_REDACT_FIELDS = {"hashed_password"}


def _dumps(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, default=str)


def _column_snapshot(obj) -> dict:
    """تصویر کامل ستون‌های یک رکورد (بدون فیلدهای حساس)."""
    mapper = inspect(obj).mapper
    return {
        col.key: getattr(obj, col.key)
        for col in mapper.columns
        if col.key not in _REDACT_FIELDS
    }


def _changed_fields(obj) -> tuple[dict, dict]:
    """فقط ستون‌هایی که واقعاً تغییر کرده‌اند → (قدیم، جدید)."""
    state = inspect(obj)
    old, new = {}, {}
    for attr in state.mapper.column_attrs:
        if attr.key in _REDACT_FIELDS:
            continue
        hist = state.attrs[attr.key].history
        if hist.has_changes():
            old[attr.key] = hist.deleted[0] if hist.deleted else None
            new[attr.key] = hist.added[0] if hist.added else None
    return old, new


@event.listens_for(SessionLocal, "after_flush")
def _write_audit_rows(session, flush_context):
    user_id = session.info.get("user_id")
    now = datetime.utcnow()
    rows = []

    def add(obj, action, old=None, new=None):
        table = obj.__table__.name
        if table in _EXCLUDE_TABLES:
            return
        rows.append(dict(
            id=models.gen_uuid(),
            table_name=table,
            record_id=str(obj.id),
            action=action,
            changed_by=user_id,
            changed_at=now,
            old_value=_dumps(old) if old is not None else None,
            new_value=_dumps(new) if new is not None else None,
        ))

    for obj in session.new:
        add(obj, "create", new=_column_snapshot(obj))

    for obj in session.dirty:
        if not session.is_modified(obj, include_collections=False):
            continue
        old, new = _changed_fields(obj)
        if new:
            add(obj, "update", old=old, new=new)

    for obj in session.deleted:
        add(obj, "delete", old=_column_snapshot(obj))

    if rows:
        # درج مستقیم با Core — در after_flush نباید session.add کرد
        session.connection().execute(models.AuditLog.__table__.insert(), rows)
