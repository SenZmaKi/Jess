import sys
from PIL import Image
from pathlib import Path
from jess.common import parent_papers_pdfs_dir, parent_papers_images_dir


def images_to_pdf(images_dir: Path):
    images: list[Image.Image] = []
    for path in images_dir.iterdir():
        img = Image.open(path)
        if img.mode != "RGB":
            img = img.convert("RGB")  
        images.append(img)

    save_file_path = parent_papers_pdfs_dir / f"{images_dir.name}.pdf"
    if images:
        images[0].save(save_file_path, save_all=True, append_images=images[1:])
        print(f"PDF created successfully at: {save_file_path}")
    else:
        print(f"No images found to convert in {images_dir}")

def main() -> None:
    dir = Path(sys.argv[1]) if len(sys.argv) > 1 else parent_papers_images_dir
    for path in dir.iterdir():
        images_to_pdf(path)

if __name__ == "__main__":
    main()