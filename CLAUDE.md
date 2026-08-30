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

## 알아둘 것

- `_includes/` `_layouts/` `_sass/` 에 Minimal Mistakes 사본이 통째로 들어 있고, 로컬 사본이 `remote_theme` 설정을 이긴다. 즉 `_config.yml` 의 `mmistakes/minimal-mistakes@4.27.3` 은 실제로 아무 일도 하지 않으며, `jekyll-remote-theme` 도 설치돼 있지 않다. 테마를 올리려면 사본을 먼저 정리해야 한다.
- `Gemfile` 의 `gemspec` 지시자가 `minimal-mistakes-jekyll.gemspec` 을, 그 gemspec 이 `package.json` 의 version 을 읽는다. 셋 다 지우려면 Gemfile 을 같이 고쳐야 한다.
- 파일은 CRLF 로 체크아웃된다. 스크립트로 본문을 다룰 때 줄바꿈을 정규화한다.
