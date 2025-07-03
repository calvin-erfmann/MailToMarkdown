# 📬 MailToMarkdown

**Export your emails as Markdown files – attachments included.**  
Perfect for archiving, searching, or importing into your [Obsidian](https://obsidian.md/) vault.

---

## 💭 Motivation

At the school where I recently graduated, every student received their own email account. Over the years, I received many useful, funny, and personal messages that I didn’t want to lose.

As a heavy Obsidian user, I wanted to keep those emails in a well-structured, searchable Markdown format – as part of my personal knowledge archive.

Instead of manually exporting every message, I built this tool (with the help of AI) to make the job easier and share it with others who might want the same – **so you don’t have to write 20 prompts just to get a usable script** 😉

---

## 🛠 Features

- Interactive command-line input (server, port, folder, etc.)
- Connects via **IMAP over SSL**
- Parses and saves each email as `.md` with metadata
- Saves attachments and links them in the Markdown
- Displays progress with a nice terminal bar
- Outputs clean, portable files for backup or import

---

## ▶️ How to Use

### 🧱 1. Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/yourusername/mailtomarkdown.git
cd mailtomarkdown
pip install -r requirements.txt

📦 requirements.txt
nginx
Kopieren
Bearbeiten
markdownify
html2text
tqdm
🚀 2. Run the script
bash
Kopieren
Bearbeiten
python export_mails.py
You’ll be asked for:

Your email address

Your password (secure input)

IMAP server (e.g. imap.example.com)

Port (usually 993)

Folder name (INBOX by default)

Output folder (e.g. email_export)

After that, the export starts. All emails are saved as .md files in the output folder, and all attachments go to attachments/.

🧠 AI-Generated Notice
This tool was written largely with the help of ChatGPT (OpenAI), guided by personal goals and needs. I’m sharing it so that others don’t need to go through the same back-and-forth to get a working solution.

Feel free to fork, improve, or adapt it 💌

📂 Example Markdown Output
markdown
Kopieren
Bearbeiten
---
from: teacher@school.de
to: calvin@example.com
date: 2024-03-12_10-23-05
subject: Final Exam Results
attachments:
  - [Grades.pdf](attachments/Grades.pdf)
---

Hi Calvin,

Attached are your results. Congrats!

Best,  
Your teacher
🖤 License
MIT – use it however you want.

☕ Author
Made with love and memory-preserving intention by Calvin Erfmann

yaml
Kopieren
Bearbeiten

---

