import subprocess
import json
import os
from datetime import datetime

OUTPUT_DIR = "../products"

PROMPT = """
You are an AI author. Write a short nonfiction ebook on a trending topic.

Respond ONLY in this format:
---
Title: [Your Book Title]
Description: [Short pitch for Gumroad]
TOC:
1. Chapter 1 Title
2. Chapter 2 Title
...
Content:
# Chapter 1 Title
Content here...

# Chapter 2 Title
Content here...
...
---
Keep it under 3000 words total.
"""

def run_ollama(model="mistral"):
    print("Running Ollama...")
    result = subprocess.run(
        ["ollama", "run", model],
        input=PROMPT.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.stdout.decode()

def save_output(text):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = f"ebook_{now}"
    path = os.path.join(OUTPUT_DIR, folder_name)
    os.makedirs(path, exist_ok=True)

    # Basic parsing
    try:
        title = text.split("Title:")[1].split("Description:")[0].strip()
        desc = text.split("Description:")[1].split("TOC:")[0].strip()
    except:
        title = "Untitled"
        desc = "No description."

    # Save everything
    with open(os.path.join(path, "content.md"), "w", encoding="utf-8") as f:
        f.write(text)
    with open(os.path.join(path, "meta.json"), "w", encoding="utf-8") as f:
        json.dump({"title": title, "description": desc}, f, indent=2)

    print(f"Saved: {path}")
    return path

if __name__ == "__main__":
    output = run_ollama()
    save_output(output)
