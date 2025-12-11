import os
bot_mail = os.getenv("bot_mail")

if __name__ == "__main__":
    from oauth import get_authorization_url
    auth = get_authorization_url(bot_mail,"")
    print(bot_mail)
    print(auth)