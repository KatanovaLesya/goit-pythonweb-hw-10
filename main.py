from fastapi import FastAPI
from routers import contacts
from routers.auth_router import router as auth_router  # ✅ правильний імпорт

app = FastAPI(
    title="📇 Contacts API",
    description="REST API для керування контактами",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Welcome to HW10 API"}

# ✅ Підключення роутера авторизації
app.include_router(auth_router, prefix="/auth")

# ✅ Підключення роутера контактів
app.include_router(contacts.router)
