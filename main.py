import os

bot_mail = os.getenv("bot_mail")

if __name__ == "__main__":
    from app.database import SessionLocal
    # from crud.credentials import save_creds, load_creds
    from crud.mail import save_mail, create_mail
    from src.mailbox import read_last_mails, format_mail
    # auth = read_last_mails(5)
    # print(bot_mail)
    # print(auth)
    with SessionLocal() as session:
        # save_creds(session, "bob", "jsonstringlol")
        # a = load_creds(session, "bob")
        # print(a)
        mails = read_last_mails(5)
        for mail in mails:
            mail_id, source, date, subject, body = format_mail(mail)
            save_mail(session, create_mail(mail_id, source, date, subject, body))
