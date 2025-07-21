import os
import markdown
import pdfkit
import json

OUTPUT_DIR = "../products"

PDF_OPTIONS = {
    'page-size': 'Letter',
    'encoding': 'UTF-8',
    'margin-top': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'margin-right': '0.75in',
}

def find_latest_product_dir():
    dirs = [os.path.join(OUTPUT_DIR, d) for d in os.listdir(OUTPUT_DIR)]
    dirs = [d for d in dirs if os.path.isdir(d)]
    return max(dirs, key=os.path.getmtime)

def convert_md_to_pdf(content_path, output_path):
    with open(content_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    html = markdown.markdown(md_content)

    # Wrap HTML with basic style
    html = f"""<html><head><style>
    body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 2em; }}
    h1, h2, h3 {{ color: #333; }}
    </style></head><body>{html}</body></html>"""

    pdfkit.from_string(html, output_path, options=PDF_OPTIONS)
    print(f"✅ Exported PDF to {output_path}")

if __name__ == "__main__":
    folder = find_latest_product_dir()
    content_path = os.path.join(folder, "content.md")
    pdf_output = os.path.join(folder, "ebook.pdf")

    if os.path.exists(content_path):
        convert_md_to_pdf(content_path, pdf_output)
    else:
        print("❌ content.md not found!")
