import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
import os
import re
from getpass import getpass
from tqdm import tqdm

# 🧼 Clean up filenames
def sanitize_filename(s):
    s = re.sub(r'[\r\n\t]', '', s)
    s = s.strip()
    s = re.sub(r'[\\/*?:"<>|]', "_", s)
    return s

# 🧠 Interactive input
print("📧 Email Export Tool")
EMAIL = input("Email address: ").strip()
PASSWORD = getpass("Password: ")
IMAP_SERVER = input("IMAP server (e.g. imap.example.com): ").strip()
IMAP_PORT = int(input("IMAP port (e.g. 993): ").strip())
IMAP_FOLDER = input("IMAP folder (e.g. INBOX): ").strip() or "INBOX"
OUTPUT_DIR = input("Output directory (e.g. email_export): ").strip() or "email_export"

# 📦 Create output directories
os.makedirs(OUTPUT_DIR, exist_ok=True)
attachments_dir = os.path.join(OUTPUT_DIR, "attachments")
os.makedirs(attachments_dir, exist_ok=True)

# 🔌 Connect to server
try:
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL, PASSWORD)
    mail.select(IMAP_FOLDER)
    print("✅ Connected successfully.")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit()

# 📥 Search for all emails
status, messages = mail.search(None, "ALL")
email_ids = messages[0].split()

exported_emails = 0
exported_attachments = 0

print(f"📬 Found {len(email_ids)} emails. Starting export...\n")

# 🧮 Progress bar
for i in tqdm(email_ids, desc="Exporting emails", unit="email"):
    res, msg_data = mail.fetch(i, "(RFC822)")
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    subject = decode_header(msg["Subject"] or "no_subject")[0][0]
    if isinstance(subject, bytes):
        subject = subject.decode(errors="ignore")
    subject = sanitize_filename(subject or "no_subject")

    from_ = msg.get("From", "unknown")
    to = msg.get("To", "unknown")
    date = msg.get("Date", "")
    try:
        date_obj = parsedate_to_datetime(date)
        date_fmt = date_obj.strftime("%Y-%m-%d_%H-%M-%S")
    except:
        date_fmt = "unknown_date"

    markdown = f"---\nfrom: {from_}\nto: {to}\ndate: {date_fmt}\nsubject: {subject}\nattachments:\n"
    body = ""
    attachment_paths = []

    for part in msg.walk():
        content_type = part.get_content_type()
        filename = part.get_filename()

        if filename:
            filename = sanitize_filename(filename)
            filepath = os.path.join(attachments_dir, filename)
            try:
                with open(filepath, "wb") as f:
                    f.write(part.get_payload(decode=True))
                attachment_paths.append(f"[{filename}](attachments/{filename})")
                exported_attachments += 1
            except Exception as e:
                print(f"⚠️ Failed to save attachment: {filename} → {e}")
        elif content_type == "text/plain":
            payload = part.get_payload(decode=True)
            if payload:
                body += payload.decode(errors="ignore")

    if not attachment_paths:
        markdown += "  - None\n"
    else:
        for link in attachment_paths:
            markdown += f"  - {link}\n"
    markdown += "---\n\n"
    markdown += body.strip()

    filename_md = f"{date_fmt}_{subject[:50]}.md"
    filepath_md = os.path.join(OUTPUT_DIR, sanitize_filename(filename_md))
    with open(filepath_md, "w", encoding="utf-8") as f:
        f.write(markdown)

    exported_emails += 1

# ✅ Summary
print("\n🎉 Export complete!")
print(f"📄 Emails exported: {exported_emails}")
print(f"📎 Attachments saved: {exported_attachments}")
