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


def check_blog():
    idx = read("blog/index.html")
    post = read("blog/ehr-response-time/index.html")
    assert "e-HR 응답 18초를 1초로 줄인 과정" in idx, "목록에 샘플 글 제목 없음"
    assert 'href="/blog/ehr-response-time/"' in idx, "목록에 샘플 글 링크 없음"
    assert "This post is written in Korean." in post and 'lang="en"' in post, "EN 안내 없음"
    for html in (idx, post):
        assert "localStorage.getItem('lang')" in html, "언어 유지 스크립트 없음"
        assert "/projects/project.css" in html and "/assets/blog.css" in html, "스타일 링크 없음"
    # summary_en이 없을 때 빈 칸 대신 한국어로 대체되어야 한다
    assert not re.search(r'<span lang="en">\s*</span>', idx), "EN 빈 칸 있음"


def check_feed():
    assert "e-HR 응답 18초를 1초로 줄인 과정" in read("feed.xml"), "피드에 샘플 글 없음"


def check_log():
    idx = read("log/index.html")
    assert "2026" in idx and "기술 블로그와 이력 로그 개설" in idx, "타임라인에 연도·샘플 로그 없음"
    read("log/blog-launch/index.html")  # URL에 날짜가 붙지 않아야 한다
    assert "기술 블로그와 이력 로그 개설" not in read("feed.xml"), "로그가 피드에 들어감"


def main():
    assert SITE.exists(), "먼저 bundle exec jekyll build 실행"
    for check in (check_existing_untouched, check_not_deployed, check_filenames,
                  check_blog, check_feed, check_log):
        check()
    print("OK")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}")
        sys.exit(1)
