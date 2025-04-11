import os
import shutil
import hashlib
import json
import time
import threading
from datetime import datetime
from plyer import notification

LOG_DIR = "logs"
NUM_THREADS = 4

def get_all_files(folder):
    file_map = {}
    for root, _, files in os.walk(folder):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, folder)
            stat = os.stat(full_path)
            file_map[rel_path] = {
                "modified": stat.st_mtime,
                "size": stat.st_size
            }
    return file_map

def compare_dirs(src, dst):
    src_files = get_all_files(src)
    dst_files = get_all_files(dst)

    changes = {
        "new": [],
        "modified": [],
        "deleted": []
    }

    for path, meta in src_files.items():
        if path not in dst_files:
            changes["new"].append((path, meta["size"]))
        elif meta["modified"] > dst_files[path]["modified"]:
            changes["modified"].append((path, meta["size"]))

    for path in dst_files:
        if path not in src_files:
            changes["deleted"].append(path)

    return changes

def summarize_changes(changes):
    total_size = sum(size for _, size in changes["new"] + changes["modified"])
    return {
        "new_files": len(changes["new"]),
        "modified_files": len(changes["modified"]),
        "deleted_files": len(changes["deleted"]),
        "total_size_bytes": total_size
    }

def save_log(changes, summary):
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(LOG_DIR, f"sync_log_{timestamp}.json")
    with open(log_path, 'w') as f:
        json.dump({"summary": summary, "changes": changes}, f, indent=2)
    print(f"Log saved to {log_path}")
    return log_path

def copy_worker(task_queue, src, dst):
    while True:
        try:
            path = task_queue.pop()
        except IndexError:
            break
        src_path = os.path.join(src, path)
        dst_path = os.path.join(dst, path)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.copy2(src_path, dst_path)
        print(f"Copied: {path}")

def delete_worker(task_queue, dst):
    while True:
        try:
            path = task_queue.pop()
        except IndexError:
            break
        dst_path = os.path.join(dst, path)
        if os.path.exists(dst_path):
            os.remove(dst_path)
            print(f"Deleted: {path}")

def sync_changes(changes, src, dst):
    copy_tasks = [path for path, _ in changes["new"] + changes["modified"]]
    delete_tasks = list(changes["deleted"])

    copy_queue = copy_tasks.copy()
    delete_queue = delete_tasks.copy()

    threads = []
    for _ in range(NUM_THREADS):
        t = threading.Thread(target=copy_worker, args=(copy_queue, src, dst))
        t.start()
        threads.append(t)

    for _ in range(NUM_THREADS):
        t = threading.Thread(target=delete_worker, args=(delete_queue, dst))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

def notify(summary):
    notification.notify(
        title="Media Sync Completed",
        message=f"Added: {summary['new_files']}, Modified: {summary['modified_files']}, Deleted: {summary['deleted_files']}",
        timeout=5
    )

def main():
    src = r"L:\Camera"
    backups = [r"H:\Camera", r"I:\Camera"]

    for dst in backups:
        print(f"\n--- Checking changes for {dst} ---")
        changes = compare_dirs(src, dst)
        summary = summarize_changes(changes)
        print("Summary:")
        print(json.dumps(summary, indent=2))

        print("\nOptions:")
        print("1 - Proceed with sync")
        print("2 - Save preview log only")
        print("3 - Sync and save log")
        choice = input("Choose an option: ")

        if choice == "2" or choice == "3":
            save_log(changes, summary)

        if choice == "1" or choice == "3":
            sync_changes(changes, src, dst)
            notify(summary)

if __name__ == "__main__":
    main()
