import os
import sys
import pdf2image


def main():
    if len(sys.argv) < 2:
        print("<pdf-path> is required")
        sys.exit(1)
    pdf_path = sys.argv[1]
    file_title = os.path.split(pdf_path)[-1].split(".")[0]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else file_title
    images = pdf2image.convert_from_path(pdf_path)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    for idx, image in enumerate(images):
        image_path = os.path.join(output_dir, f"{idx + 1}.png")
        image.save(image_path)


if __name__ == "__main__":
    main()
