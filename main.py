import os
bot_mail = os.getenv("bot_mail")

if __name__ == "__main__":
    from app.database import SessionLocal
    from crud.db_utils import save_creds, load_creds
    from src.mailbox import read_last_mails
    auth = read_last_mails(5)
    print(bot_mail)
    print(auth)
    # with SessionLocal() as session:
    #     save_creds(session, "bob", "jsonstringlol")
    #     a = load_creds(session, "bob")
    #     print(a)