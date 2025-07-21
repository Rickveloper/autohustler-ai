import subprocess
import os
import time

def run_script(name, folder="generator"):
    print(f"▶ Running {name}...")
    path = os.path.join(folder, name)
    result = subprocess.run(["python", path])
    if result.returncode != 0:
        print(f"❌ Error running {name}")
    else:
        print(f"✅ Finished {name}")

def run_all():
    run_script("ebook_writer.py")
    run_script("cover_creator.py")
    run_script("pdf_exporter.py")
    run_script("uploader.py", folder="deploy")

if __name__ == "__main__":
    run_all()
