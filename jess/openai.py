import logging
import sys
from typing import Callable
from pathlib import Path
from dotenv import load_dotenv
import openai
import base64
from io import BytesIO
from PIL import Image
from jess.common import parent_papers_answers_md_dir
import time
import pdf2image


load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OpenAI")
IMAGE_FORMAT = "jpeg"



class OpenAIException(Exception):
    pass


client = openai.OpenAI()
if not client.api_key:
    raise OpenAIException("OPENAI_API_KEY environment variable is not set.")


def print_runtime_later(task: str) -> Callable[[], None]:
    start_time = time.time()

    def print_runtime() -> None:
        elapsed_time = time.time() - start_time
        logger.info(f"Task {task} took {elapsed_time:.2f} seconds.")

    return print_runtime


def image_to_base64(image: Image.Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format=IMAGE_FORMAT.upper())
    img_byte_data = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte_data).decode("utf-8")
    return img_base64


def convert_pdf_to_images(pdf_path: Path) -> list[Image.Image]:
    logger.info(f"Converting pdfs to images: {pdf_path}")
    prt = print_runtime_later("Convert pdfs to images")
    pdf_images = [image for image in pdf2image.convert_from_path(str(pdf_path))]
    prt()
    return pdf_images


def run_prompt(paper_path: Path) -> None:
    instructions = Path("instructions.txt").read_text()
    prompt = Path("prompt.txt").read_text()
    paper_images = (
        convert_pdf_to_images(paper_path)
        if paper_path.suffix == ".pdf"
        else [Image.open(paper_image) for paper_image in paper_path.iterdir()]
    )

    prt = print_runtime_later("Encoding images to base64")
    base64_images = [image_to_base64(image) for image in paper_images]
    prt()
    logger.info(f"Prompting OpenAI with {len(base64_images)} images")
    prt = print_runtime_later("Prompting OpenAI")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    *[
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{IMAGE_FORMAT};base64,{base64_image}",
                            },
                        }
                        for base64_image in base64_images
                    ],
                ],
            },
            {
                "role": "system",
                "content": instructions,
            },
        ],
    )
    prt()
    output = response.choices[0].message.content
    if not output:
        raise OpenAIException("OpenAI response is empty.")
    logger.info(f"OpenAI response: {output}")
    answers_path = (
        parent_papers_answers_md_dir / f"{paper_path.with_suffix('.md').name}"
    )
    with open(answers_path, "w") as f:
        f.write(output)


def main() -> None:
    if len(sys.argv) < 2:
        print("<paper-paper> is required")
        sys.exit(1)
    paper_path = sys.argv[1]
    run_prompt(Path(paper_path))

if __name__ == "__main__":
    main()