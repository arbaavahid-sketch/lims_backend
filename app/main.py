"""
نقطه ورود برنامه LIMS
همه روترها اینجا به اپلیکیشن FastAPI وصل می‌شوند.
"""
from fastapi import FastAPI

from .database import Base, engine
from . import models  # noqa: F401  (لازم است تا مدل‌ها قبل از create_all شناخته شوند)
from .routers import users, samples, test_methods, results, equipment, grades

# ساخت خودکار جداول در دیتابیس هنگام شروع.
# نکته: این روش فقط برای شروع سریع مناسب است. در محیط واقعی
# به‌جای این خط از Alembic برای migration استفاده کنید.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LIMS - سیستم مدیریت اطلاعات آزمایشگاه",
    description="بک‌اند کنترل کیفیت صنعتی | FastAPI + PostgreSQL",
    version="0.1.0",
)

# وصل کردن روترها
app.include_router(users.router)
app.include_router(samples.router)
app.include_router(test_methods.router)
app.include_router(grades.router)
app.include_router(results.router)
app.include_router(equipment.router)


@app.get("/", tags=["Root"])
def root():
    """بررسی سلامت سرویس"""
    return {
        "message": "LIMS API در حال اجراست ✅",
        "docs": "/docs",
    }
