import extract_msg
import json
from pathlib import Path

input_dir = Path(r"C:\Luna\mycode\Outlook_email\Eco_batch_msg")
output_dir = Path(r"C:\Luna\mycode\Outlook_email\Eco_parse")

output_dir.mkdir(exist_ok=True)

success = 0
fail = 0

for msg_file in input_dir.glob("*.msg"):
    try:
        msg = extract_msg.Message(str(msg_file))

        email_data = {
            "file_name": msg_file.name,
            "from": msg.sender,
            "to": msg.to,
            "date": msg.date.isoformat() if msg.date else None,
            "subject": msg.subject,
            "body": msg.body
        }

        output_file = output_dir / f"{msg_file.stem}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(email_data, f, ensure_ascii=False, indent=2)

        success += 1
        print(f"✔ Saved: {msg_file.name}")

    except Exception as e:
        fail += 1
        print(f"❌ Failed: {msg_file.name} → {e}")

print("\n====== DONE ======")
print(f"Success: {success}")
print(f"Failed: {fail}")