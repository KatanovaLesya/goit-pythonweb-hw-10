from services.email_service import send_email

send_email(
    to_email="to@example.com", 
    subject="🔔 Тестовий лист від FastAPI",
    body="Вітаю! Це перевірка функції надсилання листів через Mailtrap 📬"
)
