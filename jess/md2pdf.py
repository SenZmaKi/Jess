import sys
from pathlib import Path
import markdown
import pdfkit
from jess.common import parent_papers_answers_md_dir, parent_papers_answers_pdf_dir

def main():
    dir = Path(sys.argv[1]) if len(sys.argv) > 1 else parent_papers_answers_md_dir
    for md_path in dir.iterdir():
        html = markdown.markdown(md_path.read_text())
        pdf_path = parent_papers_answers_pdf_dir / f"{md_path.with_suffix('.pdf').name}"
        pdfkit.from_string(html, pdf_path )

if __name__ == "__main__":
    main()