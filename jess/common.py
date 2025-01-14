from pathlib import Path

parent_papers_dir = Path("papers")
parent_papers_dir.mkdir(exist_ok=True)
parent_papers_images_dir = parent_papers_dir / "images"
parent_papers_images_dir.mkdir(exist_ok=True)
parent_papers_pdfs_dir = parent_papers_dir / "pdfs"
parent_papers_pdfs_dir.mkdir(exist_ok=True)
parent_papers_answers_dir = parent_papers_dir / "answers"
parent_papers_answers_dir.mkdir(exist_ok=True)
parent_papers_answers_md_dir = parent_papers_answers_dir / "md"
parent_papers_answers_md_dir.mkdir(exist_ok=True)
parent_papers_answers_pdf_dir = parent_papers_answers_dir / "pdf"
parent_papers_answers_pdf_dir.mkdir(exist_ok=True)
