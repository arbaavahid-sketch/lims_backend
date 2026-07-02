import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# مقدار DATABASE_URL را از متغیر محیطی بخوان، در غیر این صورت از SQLite محلی استفاده کن.
# SQLite برای توسعهٔ محلی است و هیچ نصبی نمی‌خواهد؛ برای محیط واقعی
# فقط کافی است DATABASE_URL را روی یک رشتهٔ اتصال PostgreSQL تنظیم کنید.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./lims_dev.db")

# SQLite در حالت چند-نخی FastAPI به این آرگومان نیاز دارد؛ برای Postgres لازم نیست.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency برای دریافت سشن دیتابیس در هر ریکوئست"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
