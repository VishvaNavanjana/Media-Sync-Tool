# 📁 Media Sync Tool

A lightweight Python tool for syncing and maintaining redundancy across multiple folders (such as photo libraries) on different hard drives.

---

## ✅ Features

- Detects **new, modified, and deleted** files between source and backup folders
- Provides a summary preview of changes
- Allows you to:
  - Just log changes
  - Sync changes
  - Sync and log changes together
- Uses **multi-threading** for fast operations
- Shows **desktop notifications** after sync
- Keeps a **JSON log** for every sync run

---

## 📦 Requirements

- Python 3.6+
- `plyer` for desktop notifications

Install dependencies using pip:

```bash
pip install plyer
🖥️ How to Use
Set source and backup paths in the main() function:

src = r"L:\Camera"
backups = [r"H:\Camera", r"I:\Camera"]
These can be paths to folders on different drives or partitions.

Run the script:

python media_sync_tool.py
For each backup location, you'll be shown:

--- Checking changes for H:\Camera ---
Summary:
{
  "new_files": 5,
  "modified_files": 3,
  "deleted_files": 1,
  "total_size_bytes": 17839523
}

Options:
1 - Proceed with sync
2 - Save preview log only
3 - Sync and save log
Choose an option:
Choose your preferred action:

1 → Proceed with syncing files only

2 → Save a JSON log of the changes without syncing

3 → Sync files and save a JSON log

📂 Logs
Logs are saved in the logs/ directory next to the script.

Each log file is timestamped and contains:

{
  "summary": {
    "new_files": 5,
    "modified_files": 3,
    "deleted_files": 1,
    "total_size_bytes": 17839523
  },
  "changes": {
    "new": [["holiday2023/photo1.jpg", 5849301]],
    "modified": [["family/photo2.png", 892341]],
    "deleted": ["old/photo3.jpg"]
  }
}
⚙️ Notes
The tool compares file last modified time to detect updates.

It uses shutil.copy2 to retain file metadata.

Threads are used to speed up copy/delete operations. Adjust NUM_THREADS to suit your system.

🚧 Limitations
No rollback or versioning in this version

GUI version is available in a different branch

Assumes folder structures are similar between source and backups

🔔 Notification Example
After sync is done, you’ll receive a system notification like:

Media Sync Completed
Added: 3, Modified: 2, Deleted: 1

📜 License
MIT License

💬 Feedback
Got suggestions or issues? Feel free to open an issue or share feedback.

---
