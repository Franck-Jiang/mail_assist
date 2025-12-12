import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_gmail_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as f:
            f.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

def read_body(payload):
    body = payload.get("body", {})

    if body.get("size", 0) == 0:
        return read_body(payload.get("parts")[0])
    else:
        return base64.urlsafe_b64decode(body.get("data", "") + '=').decode("utf-8", errors="replace")


def read_last_mails(max_results=10):
    service = get_gmail_service()
    
    results = service.users().messages().list(
        userId="me",
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])

    mails = []

    for m in messages:
        msg = service.users().messages().get(
            userId="me",
            id=m["id"],
            format="full"
        ).execute()

        snippet = msg.get("snippet")
        payload = msg.get("payload", {})
        headers = payload.get("headers", [])
        body = read_body(payload)

        subject = next((h["value"] for h in headers if h["name"] == "Subject"), None)
        sender = next((h["value"] for h in headers if h["name"] == "From"), None)

        mails.append({
            "subject": subject,
            "from": sender,
            "snippet": snippet,
            "body": body,
            "id": m["id"]
        })

    return mails

if __name__ == "__main__":
    mails = read_last_mails(5)
    for mail in mails:
        print("----")
        print("From:", mail["from"])
        print("Subject:", mail["subject"])
        print("Snippet:", mail["snippet"])
        print("Body:", mail["body"])
