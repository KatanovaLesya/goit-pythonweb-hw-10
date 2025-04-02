from fastapi import FastAPI
from routers import contacts

app = FastAPI(
    title="📇 Contacts API",
    description="REST API для керування контактами",
    version="1.0.0"
)

# Підключення router
app.include_router(contacts.router)
