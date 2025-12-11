from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models.credentials import Credentials

def save_creds(db: Session, username, json_string: str):
    new_user = Credentials(name=username, credentials_json=json_string)
    try:
        db.add(new_user)
        db.commit()
        db.flush()
        db.refresh(new_user)
    except IntegrityError as e:
        print(f"Can't add {username}")
        db.rollback()
        return e
    return new_user

def load_creds(db: Session, username):
    stmt = select(Credentials).where(Credentials.name == username)
    print(stmt)
    result = db.execute(stmt).fetchone()
    return result