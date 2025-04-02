from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from schemas import Contact, ContactCreate, ContactUpdate
from repository import contacts as repository_contacts

router = APIRouter(prefix="/contacts", tags=["contacts"])

# Залежність для отримання сесії
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Створити новий контакт
@router.post("/", response_model=Contact, status_code=status.HTTP_201_CREATED)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return repository_contacts.create_contact(db, contact)


# Отримати список контактів
@router.get("/", response_model=List[Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return repository_contacts.get_contacts(db, skip, limit)


# Отримати контакт по ID
@router.get("/{contact_id}", response_model=Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = repository_contacts.get_contact(db, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


# Оновити контакт
@router.put("/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    updated_contact = repository_contacts.update_contact(db, contact_id, contact)
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact


# Видалити контакт
@router.delete("/{contact_id}", response_model=Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    deleted = repository_contacts.delete_contact(db, contact_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return deleted


# Пошук по імені, прізвищу або email
@router.get("/search/", response_model=List[Contact])
def search_contacts(query: str, db: Session = Depends(get_db)):
    return repository_contacts.search_contacts(db, query)


# Найближчі дні народження
@router.get("/birthdays/", response_model=List[Contact])
def upcoming_birthdays(db: Session = Depends(get_db)):
    return repository_contacts.get_upcoming_birthdays(db)
