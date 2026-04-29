import extract_msg
import re
from pathlib import Path
import csv

input_dir = Path(r"C:\Luna\mycode\Outlook_email\Eco_batch_msg")
output_file = Path(r"C:\Luna\mycode\Outlook_email\subjects.csv")

def classify_by_subject(subject):
    s = (subject or "").lower()

    if "new message" in s or "new customer message" in s or "new submission" in s:
        return "inquiry"

    if "approval" in s or "approve" in s or "proof" in s:
        return "approval"

    if "billing" in s or "invoice" in s or "charged" in s:
        return "system_billing"

    if s.startswith("re:") or s.startswith("fw:") or "fwd:" in s:
        return "reply_or_forward"

    return "unknown"


rows = []

for msg_file in input_dir.glob("*.msg"):
    try:
        msg = extract_msg.Message(str(msg_file))
        body = msg.body or ""

        rows.append({
            "file_name": msg_file.name,
            "date": str(msg.date),
            "from": msg.sender,
            "to": msg.to,
            "subject": msg.subject,
            "initial_type": classify_by_subject(msg.subject),
            "body_preview": re.sub(r"\s+", " ", body[:300])
        })

    except Exception as e:
        rows.append({
            "file_name": msg_file.name,
            "date": "",
            "from": "",
            "to": "",
            "subject": "",
            "initial_type": "parse_error",
            "body_preview": str(e)
        })


with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["file_name", "date", "from", "to", "subject", "initial_type", "body_preview"]
    )
    writer.writeheader()
    writer.writerows(rows)

print(f"Saved to {output_file}")