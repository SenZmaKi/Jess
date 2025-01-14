import sys
from bs4 import BeautifulSoup, Tag
from jess.common import parent_papers_images_dir
import requests


def get(url: str, raise_on_not_ok: bool = True) -> requests.Response:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if raise_on_not_ok:
        if not response.ok:
            raise Exception(f"Got {response.status_code} response\n{response.text}")
    return response


def main() -> None:
    if len(sys.argv) < 2:
        print("<studocu-exam-url> is required")
        sys.exit(1)
    url = sys.argv[1]
    # url = "https://www.studocu.com/row/document/kenya-medical-training-college/final-qualifying-exam/fqe-pp02-kmtc-fqe-nursing/63652196?origin=relevant-from-other-courses-1"
    response = get(url)
    if not response.ok:
        raise Exception(f"Got {response.status_code} response\n{response.text}")
    with open("test.html", "w") as f:
        f.write(response.text)
    soup = BeautifulSoup(response.text, "html.parser")
    page_1_element = soup.find("img", {"class": "bi"})
    if not isinstance(page_1_element, Tag):
        raise Exception("Could not find page 1 element")
    page_1_url = page_1_element["src"]
    if not isinstance(page_1_url, str):
        raise Exception("Could not find page 1 url")
    page_no = 1
    url_split = url.split("/")
    paper_title = url_split[-2]
    course_title = url_split[-3]
    paper_dir_title = f"{paper_title}-{course_title}"
    pages_dir = parent_papers_images_dir / paper_dir_title
    pages_dir.mkdir(exist_ok=True)
    while True:
        page_url = page_1_url.replace("bg1.png", f"bg{page_no}.png")
        response = get(page_url, raise_on_not_ok=False)
        if not response.ok:
            break
        page_path = pages_dir / f"page-{page_no}.png"
        with open(page_path, "wb") as f:
            f.write(response.content)
        print(f"Saved page {page_no} image to {page_path}")
        page_no += 1
    print("Done")


if __name__ == "__main__":
    main()
