from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from database import SessionLocal
from models import User
from schemas import UserCreate, UserOut
from auth_service import get_password_hash, verify_password, create_access_token

from auth_service import get_current_user

from services.email_service import send_email
from auth_service import create_verification_token

from jose import JWTError, jwt
from fastapi import Query
from fastapi import Request
from auth_service import SECRET_KEY, ALGORITHM

from rate_limiter import limiter


router = APIRouter(tags=["auth"])




# 🧩 Залежність для доступу до БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Створення токена підтвердження
    verification_token = create_verification_token(new_user.email)

    # 🔗 Формування посилання підтвердження (в реальному проекті — з фронтендом)
    verification_link = f"http://localhost:8000/auth/verify-email?token={verification_token}"

    # Надсилання листа
    send_email(
        to_email=new_user.email,
        subject="🎉 Підтвердіть вашу пошту",
        body=f"Привіт, {new_user.username}!\n\nПерейдіть за посиланням для підтвердження вашої електронної адреси:\n{verification_link}"
    )


    return new_user


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 🔒 Перевірка верифікації
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified"
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
@limiter.limit("5/minute")
def read_users_me(request: Request, current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/verify-email")
def verify_email(token: str = Query(...), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        return {"message": "Email already verified"}

    user.is_verified = True
    db.commit()
    return {"message": "Email successfully verified!"}

