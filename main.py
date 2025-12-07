if __name__ == "__main__":
    from oauth import get_authorization_url
    auth = get_authorization_url("franck.preprod@gmail.com","")
    print(auth)