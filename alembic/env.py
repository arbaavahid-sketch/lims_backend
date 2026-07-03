"""پیکربندی Alembic — به تنظیمات خود اپ متصل است.

آدرس دیتابیس از app.database (متغیر محیطی DATABASE_URL یا SQLite محلی)
خوانده می‌شود و متادیتای مدل‌ها برای autogenerate استفاده می‌شود.
"""
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

from app.database import Base, DATABASE_URL
from app import models  # noqa: F401  — تا همهٔ جداول در متادیتا شناخته شوند

config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """اجرای مهاجرت‌ها بدون اتصال زنده (تولید SQL)."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        render_as_batch=DATABASE_URL.startswith("sqlite"),
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """اجرای مهاجرت‌ها با اتصال زنده."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            # SQLite از ALTER TABLE کامل پشتیبانی نمی‌کند؛ حالت batch لازم است
            render_as_batch=DATABASE_URL.startswith("sqlite"),
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
