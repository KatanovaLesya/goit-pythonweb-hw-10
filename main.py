from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from routers import contacts
from routers.auth_router import router as auth_router

class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(self, tokenUrl: str):
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl})
        super().__init__(flows=flows)

# 🔐 Створюємо інстанс FastAPI з описом безпеки
app = FastAPI(
    title="📇 Contacts API",
    description="REST API для керування контактами",
    version="1.0.0",
    openapi_tags=[{"name": "auth", "description": "Аутентифікація"}]
)

# 🔗 Додаємо CORS (вимога з ТЗ)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to HW10 API"}

# 🔗 Підключення роутерів
app.include_router(auth_router, prefix="/auth")
app.include_router(contacts.router)
