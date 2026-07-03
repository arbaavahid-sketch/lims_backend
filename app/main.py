"""
نقطه ورود برنامه LIMS
همه روترها اینجا به اپلیکیشن FastAPI وصل می‌شوند.
"""
from fastapi import FastAPI

from . import models  # noqa: F401
from . import audit  # noqa: F401  — فعال‌سازی AuditLog خودکار (17025 بند 8.4)
from .routers import users, samples, test_methods, results, equipment, grades, audit_logs

# ساختار دیتابیس با Alembic مدیریت می‌شود (نه create_all):
#   python -m alembic upgrade head

app = FastAPI(
    title="LIMS — Petroleum QC Laboratory / سیستم مدیریت اطلاعات آزمایشگاه نفتی",
    description="Bilingual (FA/EN) LIMS backend for refinery & petrochemical QC labs — ISO/IEC 17025 aligned",
    version="0.6.0",
)

# CORS — اجازهٔ تماس فرانت‌اند (Vite dev server) با API
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# وصل کردن روترها
app.include_router(users.router)
app.include_router(samples.router)
app.include_router(test_methods.router)
app.include_router(grades.router)
app.include_router(results.router)
app.include_router(equipment.router)
app.include_router(audit_logs.router)


@app.get("/", tags=["Root"])
def root():
    """بررسی سلامت سرویس / Service health check"""
    return {
        "message": {"fa": "LIMS API در حال اجراست ✅", "en": "LIMS API is running ✅"},
        "docs": "/docs",
    }
