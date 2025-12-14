from sqlalchemy import select
from sqlalchemy.orm import Session
from models.mail import Mail
from utils.conversion import format_datetime
def create_mail(mail_id, source, date, subject, body) -> Mail:
    return Mail(mail_id=mail_id, source=source, date=format_datetime(date), subject=subject, body=body)
    
def save_mail(db: Session, mail: Mail):
    try:
        db.add(mail)
        db.commit()
        db.flush()
        db.refresh(mail)
        print(f"Added {mail.mail_id}") #TODO logging
    except Exception as e:
        print(f"Can't add Mail: {e}")
        db.rollback()
        return e

def load_mail(db: Session, id):
    stmt = select(Mail).where(Mail.mail_id == id)
    result = db.execute(stmt).fetchone()
    return result