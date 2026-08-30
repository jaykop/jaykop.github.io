# jaykop.github.io

정주용(jaykop)의 개발 블로그. Jekyll + Minimal Mistakes, GitHub Pages 로 배포한다.

**독자는 해외(일본·서구권) 게임 스튜디오 채용자다.** 취미 블로그가 아니라 포트폴리오다. 무엇을 넣고 뺄지 애매하면 "이걸 채용자가 봤을 때 도움이 되나"로 판단한다.

> 일반 채팅 Claude 와 Claude Code 가 같은 맥락을 보도록 이 파일을 저장소에 둔다.
> 채팅 쪽에서는 raw URL 로 읽는다:
> `https://raw.githubusercontent.com/jaykop/jaykop.github.io/master/CLAUDE.md`

## 절대 지킬 것

- **커밋·푸시는 지시가 있을 때만.** 작업은 working tree 에만 반영하고 멈춘다.
- **글 본문을 임의로 고치지 않는다.** 문장은 글쓴이 목소리다. 고칠 곳을 찾으면 보고하고 승인을 받는다.
- **회사·프로젝트 코드네임을 저장소에 넣지 않는다.** 이 저장소는 공개다. 사내 경로·Jira·Confluence 식별자, 재직사 내부 정보가 커밋에 들어가면 안 된다.
- **검색엔진 비노출을 유지한다.** `_includes/head/custom.html` 의 `noindex, nofollow` 를 지우지 않는다. `robots.txt` 는 `Allow: /` 그대로 둔다 — 여기서 크롤러를 막으면 구글이 `noindex` 를 볼 수 없어 이미 색인된 페이지가 안 빠진다.

## 구조

```
_posts/<대분류>/<소분류>/YYYY-MM-DD-Slug.md   글 252편
_drafts/                                      미완성 글 (일반 빌드에서 제외)
_pages/                                       카테고리 페이지 (permalink 명시)
assets/images/<글-slug>/01.png                글 하나에 폴더 하나
.claude/skills/                               new-post · devlog-check
```

### 카테고리 — 정확히 2단계

| 대분류 | 소분류 |
|---|---|
| `unreal` | `combat` `character` `camera` `ai` `perf` `framework` `engine-internals` |
| `fundamentals` | `cpp` `graphics` `design-pattern` |
| `archive` | `game-ai-theory` |
| `post` | `CSharp` `Unity` `OS` `Network` `Math` `misc` |
| `project` | `academic` `side` `disney_pop` |

새 글은 `unreal` 또는 `fundamentals` 로 간다. 나머지는 과거 글의 자리다.

### 네비게이션

상위 탭은 주제 축 하나다 — **About · Unreal Engine · Fundamentals · Archive**. 하위 탭은 알파벳 순. `_data/navigation.yml` 에서 관리한다.

## 규약

- **제목 접두사를 반드시 붙인다.** `[DevNote]` 는 실제로 작업한 프로젝트에서 겪은 일에만, 엔진 학습 정리는 `[Unreal]`. 이 구분이 실무 경험을 가리키는 유일한 표시다.
- **이미지는 글 단위 폴더에 번호로.** `assets/images/<글-slug>/01.png`. alt 텍스트를 반드시 채운다 — 파일명이 번호라 alt 가 뜻을 담는 유일한 자리다.
- **코드블록**은 언어 태그 `c++` `csharp` `javascript` `bash` `yaml` 만 쓴다 (`c` `cs` `c#` `cpp` `js` 별칭 금지). 들여쓰기 2칸, 탭 금지.
- **미완성 글은 `_drafts/` 로.** 확장자를 지우거나 파일명을 비틀어 숨기지 않는다 — Jekyll 이 정적 파일로 흘려보낼 뿐이라 도구가 건드리면 그대로 발행된다.
- **다른 글 링크는 절대 URL** — `https://jaykop.github.io/fundamentals/cpp/Casting/`. 카테고리를 옮기면 조용히 깨지므로 아래 점검을 돌린다.

## 작업 흐름

```bash
./run.sh                                                   # 로컬 서버 http://127.0.0.1:4000
bundle exec jekyll build                                   # _site 갱신 (링크 검사에 필요)
python .claude/skills/devlog-check/devlog_check.py --all    # 전체 점검
```

`_config.yml` 은 `jekyll serve` 가 감시하지 않는다. 고쳤으면 서버를 껐다 켜야 반영된다.

스킬 두 개가 있다 — `new-post` 로 새 글 뼈대를 잡고, `devlog-check` 로 발행 전 점검한다.

## 다국어

- 본문은 한국어. `_config.yml` 의 defaults 가 모든 글·페이지에 `lang: ko` 를 준다.
- 영문판은 같은 이름에 `.en.md` 를 붙이고 `permalink: /en/<경로>/` 와 `lang: en` 을 적는다. 예: `_pages/about.en.md` → `/en/about/`.
- `_layouts/default.html` 이 `page.lang` 을 `site.locale` 보다 우선해 `<html lang>` 에 쓴다.
- 전체 번역은 하지 않는다. 채용자에게 값이 큰 것부터 — About, 그다음 잘 쓴 `[DevNote]` 몇 편.
- 플러그인(`jekyll-polyglot`)은 아직 넣지 않았다. 번역이 쌓이면 그때 옮겨도 이 `lang` front matter 를 그대로 읽으므로 이월 비용이 없다.

## 테마

`remote_theme: mmistakes/minimal-mistakes@4.27.3` 을 `jekyll-remote-theme` 으로 실제로 받아 쓴다. 로컬에는 **손댄 13개만** 남아 테마 파일을 덮어쓴다.

```
_includes/  archive-single.html · copyright.html · copyright.js
            footer/custom.html · head/custom.html · gallery
_layouts/   default.html · home.html · posts.html
_sass/minimal-mistakes/  _copyright.scss · _utilities.scss · _variables.scss · skins/_air.scss
```

테마 파일을 고쳐야 하면 upstream 원본을 그 자리에 복사한 뒤 고친다. 무엇이 다른지는 언제든 확인할 수 있다:

```bash
git fetch upstream
git diff --name-only 4.27.3 -- _includes _layouts _sass
```

## 알아둘 것

- `assets/js/` 는 4.27.1 시절 사본이 남아 테마 것을 덮어쓴다. upstream 과 다르므로 지워도 안전한지 증명되지 않았고, 빌드 경고(`lunr-en.js` conflict) 한 줄이 유일한 증상이다. JS 를 4.27.3 으로 올리고 싶을 때만 손댄다.
- `assets/css/main.scss` 의 Sass `lighten()` deprecation 경고 223건은 테마 쪽 코드에서 난다. 빌드는 통과하므로 쫓지 않는다.
- `_config.yml` 은 `jekyll serve` 가 감시하지 않는다. 고쳤으면 서버를 껐다 켠다.
- 파일은 CRLF 로 체크아웃된다. 스크립트로 본문을 다룰 때 줄바꿈을 정규화한다.
- 배포는 `.github/workflows/jekyll.yml` 이 프로젝트 Gemfile 로 직접 빌드한다. GitHub Pages 의 플러그인 화이트리스트에 묶이지 않으므로 어떤 젬이든 쓸 수 있다. `build.yml` 과 `bad-pr.yml` 은 fork 잔재로, 저장소 조건이 안 맞아 실행되지 않는다.
