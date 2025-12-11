import os
bot_mail = os.getenv("bot_mail")

if __name__ == "__main__":
    # from oauth import get_authorization_url
    # auth = get_authorization_url(bot_mail,"")
    # print(bot_mail)
    # print(auth)
    from app.database import SessionLocal
    from crud.db_utils import save_creds, load_creds
    with SessionLocal() as session:
        # save_creds(SessionLocal, "bob", "jsonstringlol")
        a = load_creds(session, "bob")
        print(a)