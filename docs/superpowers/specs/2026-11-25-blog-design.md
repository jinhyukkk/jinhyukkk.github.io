# 블로그·이력 로그 설계

작성일: 2026-11-25

## 1. 목적

- **기술 글**: 포트폴리오를 보는 채용 담당자가 프로젝트 설명에서 바로 이어서 기술 글을 읽게 한다.
- **이력 로그**: 발표, 출시, 자격증, 수상 같은 주요 이벤트를 짧은 글로 남긴다. 나중에 이력서와 경력기술서를 고칠 때 근거로 쓴다.

성공의 기준은 두 가지다.
1. 프로젝트 페이지에서 관련 글로 이동할 수 있다.
2. 새 글을 쓸 때 Markdown 파일 하나만 push하면 된다.

## 2. 목표, 비목표, 피해야 할 것

| 구분 | 내용 |
|---|---|
| 목표 | `/blog/` 기술 글 목록, `/log/` 연도별 타임라인, 글 상세 페이지, 프로젝트 페이지 하단 "관련 글", RSS, sitemap |
| 비목표 | Tistory 글 이전 (나중에 하나씩 직접 옮김), 댓글, 검색, 조회수, 글 전문 영문화 |
| 피해야 할 것 | 기존 `index.html`, `resume.html`, `projects/*.html`의 디자인이나 동작이 바뀌는 것. 기존 URL이 깨지는 것. 민감한 사내 정보가 공개 저장소에 올라가는 것 |

## 3. 제약

- 호스팅은 GitHub Pages (`jinhyukkk.github.io`, main 브랜치, 공개 저장소)다.
- 빌드는 GitHub Pages에 내장된 Jekyll이 한다. Actions 워크플로는 쓰지 않는다. 그래서 플러그인은 GitHub Pages 허용 목록에 있는 것만 쓸 수 있다.
- 기존 페이지는 front matter가 없는 순수 HTML이다. 이 파일들은 Jekyll이 손대지 않고 그대로 복사한다. 확인 결과 `{{`나 `{%` 같은 Liquid 문법과 충돌하는 문자열도 없다.
- 디자인 토큰은 `projects/project.css`와 `index.html`에 들어 있는 CSS 변수(`--bg`, `--ink`, `--accent`, Newsreader, Noto Serif KR, IBM Plex Mono)다.
- 다국어 처리 방식: `html[data-lang]` 값과 요소의 `lang="ko|en"` 속성을 조합하고, 선택값을 `localStorage('lang')`에 저장한다.
- 로컬에 Ruby와 Jekyll이 설치되어 있지 않다. 현재 `.claude/launch.json`은 `python -m http.server`만 실행한다.

## 4. 검토한 방식

| 방식 | 장점 | 단점 | 결론 |
|---|---|---|---|
| **A. Jekyll (GitHub Pages 기본)** | 기존 페이지를 건드리지 않음. 빌드 파이프라인 없음. Markdown 글은 나중에 다른 도구로도 재사용 가능 | Liquid 문법이 투박함. 플러그인은 허용 목록만 사용 가능 | **선택** |
| B. Astro + Actions | 컴포넌트 재사용과 확장성이 좋음 | Node 빌드와 워크플로를 관리해야 함. 지금 규모에 비해 과함 | 제외 |
| C. HTML 직접 작성 | 도구가 필요 없음 | 글 목록과 태그를 손으로 관리해야 해서 글이 쌓이면 유지할 수 없음 | 제외 |

"Jekyll을 쓰면 디자인이 자유롭지 않다"는 우려도 검토했다. 레이아웃은 직접 쓴 HTML/CSS라서 디자인 제약은 없다. 제약은 빌드 로직(플러그인 허용 목록)에만 있다.

## 5. 결정 사항

### 5.1 언어
- **기술 글(`tech`)**: 본문은 한국어로 쓴다. front matter에 `title_en`, `summary_en`을 둔다. EN 모드일 때 목록과 상세 페이지 헤더는 영어로 보여 주고, 본문 위에 "This post is written in Korean." 안내를 띄운다.
- **이력 로그(`log`)**: 한국어만 쓴다.
- 영어 전문이 꼭 필요한 글은 예외로 별도 파일을 만든다. 이번 범위에서는 구현하지 않지만 구조가 막지 않게 한다.

### 5.2 공개 범위
- `/log/`는 공개 페이지다. 공개해도 되는 이벤트만 짧게 요약해서 쓴다.
- 장애 상세, 사내 수치, 개인 회고 같은 민감한 원본은 이 저장소 밖에 둔다.

### 5.3 콘텐츠 모델
두 종류의 글은 폴더로 나눈다. Jekyll은 퍼머링크와 `jekyll-feed`를 직접 만든 front matter 값으로 나눌 수 없기 때문이다. [빌더 검토 반영]

| 종류 | 위치 | Jekyll에서의 형태 |
|---|---|---|
| 기술 글 | `_posts/YYYY-MM-DD-slug.md` | 기본 posts. `site.posts`로 읽히고 `/feed.xml`에는 이것만 들어감 |
| 이력 로그 | `_log/YYYY-MM-DD-slug.md` | 컬렉션(`output: true`). `site.log`로 읽힘. 날짜는 front matter의 `date`로 지정 |

기술 글의 front matter:

```yaml
---
title: e-HR 응답 18초를 1초로 줄인 과정
title_en: Cutting e-HR response from 18 s to 1 s   # tech만, 선택
summary: 실행 계획 고정과 캐시로 병목을 걷어낸 기록   # tech만, 목록에 노출
summary_en: How fixed plans and caching removed the bottleneck
project: ehr          # 선택. projects/<값>.html 파일명과 같은 값
tags: [oracle, performance]
---
```

- `log` 글에는 `title`, `date`, 선택 항목인 `project`와 짧은 본문만 있으면 된다.
- `project` 값으로 쓸 수 있는 것: `ehr`, `eland-folder-mall`, `foodcare-cle`, `group-ai-platform`, `hl-science-mall`, `investment-review-agent`, `smilegate-global`, `wegive`

### 5.4 URL

| 경로 | 내용 |
|---|---|
| `/blog/` | `_posts` 글 목록 (최신순, 제목, 요약, 날짜, 태그) |
| `/blog/<slug>/` | 기술 글 상세 |
| `/log/` | `_log` 글을 연도별로 묶은 타임라인 |
| `/log/<slug>/` | 로그 상세 (본문이 짧으면 타임라인에서 바로 펼쳐 보여도 됨) |
| `/feed.xml` | RSS (`_posts`만 들어가므로 자동으로 tech만 나감) |

퍼머링크는 전역 설정을 `permalink: /blog/:title/`로 두고, `_log` 컬렉션은 `collections.log.permalink: /log/:name/`으로 지정한다.

### 5.5 기존 사이트와 연결
- `index.html` 사이드바 nav에 `Blog`와 `Log` 링크를 추가한다. 하단 독(`.dock`)에도 Blog 아이콘을 하나 추가해서 모바일에서도 들어갈 수 있게 한다. [내 판단]
- 기존 Tistory 아이콘 링크는 유지하되, `title`/`aria-label`을 "Blog"에서 "Tistory"로 바꿔 새 Blog 링크와 겹치지 않게 한다. [내 판단]
- 프로젝트 페이지 "관련 글"에는 tech와 log를 모두 보여 준다. tech를 먼저, log는 날짜와 함께 `LOG` 라벨을 달아 보여 준다. EN 모드에서는 tech는 `title_en`(없으면 `title`), log는 한국어 제목 그대로 보여 준다. [내 판단]
- `projects/*.html`에는 빈 front matter(`---\n---`)를 추가하고, `</body>` 앞에 `{% include related.html project="<파일명>" %}`를 넣는다. 관련 글이 없으면 아무것도 출력하지 않는다. 바뀌는 것은 이 두 가지뿐이고 나머지 마크업은 그대로다.
- `index.html`과 `resume.html`은 nav 링크 외에는 Jekyll 처리 대상으로 만들지 않는다.

### 5.6 디자인
- 새 레이아웃(`_layouts/post.html`, `_layouts/list.html`)은 `projects/project.css`의 톤을 따른다. 상단 바의 `← BACK`과 KO/EN 토글, 784px 본문 폭이 기준이다.
- Markdown 본문용 스타일(코드 블록, 인용, 표, 이미지)을 추가한다. 코드 하이라이트는 Rouge 출력 class에 맞춰 기존 팔레트로 색을 지정한다.
- KO/EN 토글 스크립트는 프로젝트 페이지의 것을 `_includes`로 옮겨 재사용한다. 기존 프로젝트 페이지 안의 스크립트는 그대로 둔다.

### 5.7 설정
- `_config.yml`: `permalink`, `exclude`(`docs/`, `files/`, `README.md`). `.claude/`는 점으로 시작하는 폴더라 원래 무시된다, 플러그인 `jekyll-feed`, `jekyll-sitemap`, `jekyll-seo-tag`.
- 초안은 `_drafts/`에 둔다. 빌드 결과에는 나오지 않지만 **push하면 공개 저장소에서 원문이 보인다.** 민감한 내용은 처음부터 이 저장소에 두지 않는다.
- `.gitignore`에 `files/`를 추가한다. 지금 untracked 상태인 이력서·경력기술서 원본이 실수로 커밋되는 것을 막기 위해서다. `exclude`는 빌드 결과에서만 빼 줄 뿐 저장소 공개 여부와는 관계없다. `docs/`는 설계 문서를 커밋하므로 무시 목록에 넣지 않고 `exclude`로만 뺀다.

## 6. 빌더에게 맡기는 것

- 목록과 타임라인의 세부 레이아웃 (기존 톤 안에서)
- `_includes` 조각을 어떻게 나눌지
- 로컬 미리보기 방법 (Ruby 설치, Docker `jekyll/jekyll` 이미지, 브랜치에 push 후 확인 중 택일). 운영 빌드는 GitHub가 한다.
- 첫 샘플 글 1편과 로그 1건 (구조 검증용)
