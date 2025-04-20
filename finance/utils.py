import json, pathlib
from django.conf import settings
from .models import Entry

DATA_DIR  = pathlib.Path(settings.BASE_DIR) / "data"
DATA_DIR.mkdir(exist_ok=True)

TXT_FILE  = DATA_DIR / "finance_data.txt"
JSON_FILE = DATA_DIR / "finance_data.json"

def dump_entries_to_files():
    entries = Entry.objects.all().values()

    """
    This function dumps the entries to a JSON file and a CSV file.
    The JSON file contains all the entries in a list format.
    The CSV file contains the entries in a comma-separated format.
    The CSV file is structured with the following columns:
    - type: The type of entry (income or expense)
    - source: The source of the entry (for income)
    - description: The description of the entry
    - category: The category of the entry (for expense)
    - amount: The amount of the entry
    - date: The date of the entry
    - user: The user who created the entry
    """
    JSON_FILE.write_text(json.dumps(list(entries), default=str, indent=2))

    lines = ["type,source,description,category,amount,date,user"]
    for e in entries:
        lines.append(",".join(map(str, [
            e["entry_type"], e["source"], e["description"],
            e["category"],  e["amount"], e["date"], e["user_id"]
        ])))
    TXT_FILE.write_text("\n".join(lines))
