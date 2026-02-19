import os
import time
import json
import hashlib

def file_hash(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        return None

def repo_fingerprint(path="."):
    h = hashlib.sha256()
    for root, _, files in os.walk(path):
        for f in files:
            if ".git" in root or "__pycache__" in root:
                continue
            try:
                file_path = os.path.join(root, f)
                with open(file_path, "rb") as file:
                    h.update(file.read())
            except:
                pass
    return h.hexdigest()

def count_files(path="."):
    count = 0
    for root, _, files in os.walk(path):
        if ".git" in root or "__pycache__" in root:
            continue
        count += len(files)
    return count

# Capture specific security-relevant hashes
workflow_hash = file_hash(".github/workflows/ci.yml")
requirements_hash = file_hash("requirements.txt")

log_entry = {
    "timestamp": time.time(),
    "commit": os.getenv("GITHUB_SHA"),
    "file_count": count_files(),
    "repo_fingerprint": repo_fingerprint(),
    "workflow_hash": workflow_hash,
    "requirements_hash": requirements_hash
}

log_file = "forensic_log.jsonl"

with open(log_file, "a") as f:
    f.write(json.dumps(log_entry) + "\n")

print("Forensic log entry recorded:")
print(json.dumps(log_entry, indent=2))
