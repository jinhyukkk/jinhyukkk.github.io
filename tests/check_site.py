"""빌드 결과(_site)와 원본 파일을 검사한다. 사용법: bundle exec jekyll build 후 python tests/check_site.py"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"
NAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.md$")


def read(rel: str) -> str:
    p = SITE / rel
    assert p.exists(), f"{rel} 없음"
    return p.read_text(encoding="utf-8")


def check_existing_untouched():
    # front matter 없는 기존 페이지는 Jekyll이 손대지 않아야 한다
    for name in ("index.html", "resume.html"):
        assert (SITE / name).read_bytes() == (ROOT / name).read_bytes(), f"{name} 빌드 결과가 원본과 다름"


def check_not_deployed():
    for rel in ("files", "docs", "tests", "Gemfile", ".superpowers"):
        assert not (SITE / rel).exists(), f"{rel} 이(가) 배포됨"


def check_filenames():
    for folder in ("_posts", "_log"):
        d = ROOT / folder
        if not d.exists():
            continue
        for f in d.glob("*.md"):
            assert NAME_RE.match(f.name), f"파일명 규칙 위반: {folder}/{f.name}"


def main():
    assert SITE.exists(), "먼저 bundle exec jekyll build 실행"
    for check in (check_existing_untouched, check_not_deployed, check_filenames):
        check()
    print("OK")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}")
        sys.exit(1)
