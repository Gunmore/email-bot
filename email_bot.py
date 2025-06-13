import smtplib
import imapclient
import pyzmail
from email.message import EmailMessage
from email_validator import validate_email, EmailNotValidError

# --- CONFIGURATION ---
EMAIL_ADDRESS = 'barakamorgan26@gmail.com'
EMAIL_PASSWORD = 'zjgc dddg bidj eevd'  # Gmail App Password
IMAP_SERVER = 'imap.gmail.com'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# --- SEND EMAIL ---
def send_email(to_address, subject, body):
    try:
        validate_email(to_address)
        msg = EmailMessage()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.set_content(body)
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"Email sent to {to_address}")
    except EmailNotValidError as e:
        print(f"Invalid email address: {e}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# --- RECEIVE EMAILS ---
def check_inbox():
    try:
        with imapclient.IMAPClient(IMAP_SERVER) as client:
            client.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            client.select_folder('INBOX', readonly=True)
            messages = client.search(['UNSEEN'])
            for uid in messages:
                raw_message = client.fetch([uid], ['BODY[]', 'FLAGS'])
                message = pyzmail.PyzMessage.factory(raw_message[uid][b'BODY[]'])
                subject = message.get_subject()
                from_ = message.get_addresses('from')
                print(f"New email from {from_}: {subject}")
                # Add automation/processing logic here
    except Exception as e:
        print(f"Failed to check inbox: {e}")

def chat_mode():
    print("\n--- Email Bot Terminal Chat ---")
    print("Type 'exit' as the recipient to quit.")
    while True:
        to_address = input("To: ")
        if to_address.lower() == 'exit':
            break
        subject = input("Subject: ")
        body = input("Message: ")
        send_email(to_address, subject, body)

if __name__ == "__main__":
    mode = input("Type 'chat' for chat mode or 'inbox' to check inbox: ").strip().lower()
    if mode == 'chat':
        chat_mode()
    else:
        check_inbox()
