import os
import base64
import re
from rich.pretty import pprint as print
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
        mails.append(msg)

    return mails

def decode_data(data: str):
    return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

def extract_body(payload):

    if payload.get("body", {}).get("data"):
        return decode_data(payload["body"]["data"])

    for part in payload.get("parts", []):
        mime = part.get("mimeType", "")

        if mime == "text/plain":
            return decode_data(part["body"].get("data"))

    for part in payload.get("parts", []):
        mime = part.get("mimeType", "")

        if mime in ["multipart/alternative", "multipart/related", "multipart/mixed"]:
            return extract_body(part)

    raise Exception(f"extract_body Error: {payload}")

def format_mail(mail: dict):
    raw_body = mail.get("payload", {})
    raw_text = extract_body(raw_body)

    source = re.search(r"^De :\s+.*$", raw_text, re.MULTILINE)
    if source:
        source = source.group()
    
    date = re.search(r"^Envoyé :\s+.*$", raw_text, re.MULTILINE)
    if date:
        date = date.group()
    
    subject = re.search(r"^Objet :\s+.*$", raw_text, re.MULTILINE)
    if subject:
        subject = subject.group()

    mail_id = ""
    for header in raw_body.get("headers", []):
        if header.get("name", "") == "Message-ID":
            mail_id = header.get("value", "")
    return mail_id, source, date, subject, raw_text


if __name__ == "__main__":
    mails = read_last_mails(5)
    for mail in mails:
        mail_id, source, date, subject, body = format_mail(mail)
        print((source, date, subject))

