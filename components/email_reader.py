import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
IMAP_SERVER = os.getenv("IMAP_SERVER")

# Connect to mail server
mail = imaplib.IMAP4_SSL(IMAP_SERVER)

# Login
mail.login(EMAIL_USER, EMAIL_PASS)

# Select inbox
mail.select("inbox")

# Search all emails
status, messages = mail.search(None, "ALL")

email_ids = messages[0].split()

# Get last 10 emails
latest_ids = email_ids[-10:]

emails = []

for eid in reversed(latest_ids):
    status, msg_data = mail.fetch(eid, "(RFC822)")
    raw_email = msg_data[0][1]

    msg = email.message_from_bytes(raw_email)

    # Decode sender
    sender, encoding = decode_header(msg.get("From"))[0]
    if isinstance(sender, bytes):
        sender = sender.decode(encoding or "utf-8", errors="ignore")

    # Decode subject
    subject, encoding = decode_header(msg.get("Subject"))[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8", errors="ignore")

    date = msg.get("Date")

    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode(errors="ignore")
                except:
                    pass
                break
    else:
        try:
            body = msg.get_payload(decode=True).decode(errors="ignore")
        except:
            body = ""

    emails.append({
        "sender": sender,
        "subject": subject,
        "date": date,
        "body": body
    })

# Logout
mail.logout()

# Demo: print last 5 emails with subject + body
print("\nLast 5 Emails:\n")

for i, msg in enumerate(emails[:5]):
    subject = msg.get("subject", "No subject")
    body = msg.get("body", "")

    print(f"\nEmail {i+1}")
    print(f"Subject: {subject}")
    print(f"Body:\n{body[:200] if body else 'No content'}")