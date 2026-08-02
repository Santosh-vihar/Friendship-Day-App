"""
Persistent visitor storage using CSV.
"""

import csv
from pathlib import Path
from datetime import datetime

DB_PATH = Path("database/visitors.csv")
HEADERS = [
    "first_name", "surname", "full_name", "visit_timestamp",
    "photo_uploaded", "video_filename"
]

def init_db():
    """Create CSV file with headers if it doesn't exist."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        with open(DB_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)

def _read_all():
    """Return list of dicts for all visitors."""
    if not DB_PATH.exists():
        return []
    with open(DB_PATH, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def _write_all(rows: list[dict]):
    """Overwrite CSV with provided rows."""
    with open(DB_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)

def check_visitor(first_name: str, surname: str) -> tuple[bool, dict | None]:
    """
    Check if a visitor with the given first name and surname already exists.
    Returns (True, record_dict) if found, else (False, None).
    """
    rows = _read_all()
    for row in rows:
        if row["first_name"].strip().lower() == first_name.strip().lower() and \
           row["surname"].strip().lower() == surname.strip().lower():
            return True, row
    return False, None

def save_visitor(first_name: str, surname: str, full_name: str,
                 timestamp: str, photo_uploaded: bool, video_filename: str):
    """Add a new visitor record."""
    rows = _read_all()
    rows.append({
        "first_name": first_name,
        "surname": surname,
        "full_name": full_name,
        "visit_timestamp": timestamp,
        "photo_uploaded": str(photo_uploaded),
        "video_filename": video_filename
    })
    _write_all(rows)

def update_visitor_video(first_name: str, surname: str, video_filename: str):
    """Update the video_filename field for an existing visitor."""
    rows = _read_all()
    for row in rows:
        if row["first_name"].strip().lower() == first_name.strip().lower() and \
           row["surname"].strip().lower() == surname.strip().lower():
            row["video_filename"] = video_filename
            row["photo_uploaded"] = "True"
            break
    _write_all(rows)
