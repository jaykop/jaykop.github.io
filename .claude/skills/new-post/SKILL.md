---
name: new-post
description: devlog 에 새 글을 만드는 스킬. front matter · 파일명 · 카테고리 · 이미지 폴더를 사이트 규약대로 잡아준다. 미완성 글을 숨기는 올바른 방법(_drafts)도 여기 있다. "새 글", "포스트 작성", "글 하나 만들어줘", "초안 잡아줘" 등에 사용.
---

<!-- devlog-check: ignore -->

# New Post

새 글의 뼈대를 사이트 규약에 맞춰 만든다. 다 쓴 뒤에는 `devlog-check` 로 점검한다.

## Step 1 — 자리 정하기

### 발행할 글인가, 아직인가

| 상태 | 위치 | 파일명 |
|---|---|---|
| 발행 | `_posts/<대분류>/<소분류>/` | `YYYY-MM-DD-Slug.md` |
| 미완성 | `_drafts/` | `Slug.md` (날짜 없어도 된다) |

**미완성 글은 반드시 `_drafts/` 로 간다.** 확장자를 지우거나 파일명을 비틀어 숨기지 않는다 — Jekyll 은 그런 파일을 글이 아니라 정적 파일로 흘려보낼 뿐이라, 의도대로 숨겨지는 게 우연이고 나중에 도구가 건드리면 그대로 발행된다. `_drafts/` 는 일반 빌드에서 제외되고 `jekyll serve --drafts` 로만 보인다.

### 카테고리 — 정확히 2단계

| 대분류 | 소분류 | 무엇 |
|---|---|---|
| `unreal` | `combat` `character` `camera` `ai` `perf` `framework` `engine-internals` | 언리얼 |
| `fundamentals` | `cpp` `graphics` `design-pattern` | 언어·CS 기초 |
| `archive` | `game-ai-theory` | 옛 이론 정리 |
| `post` | `CSharp` `Unity` `OS` `Network` `Math` `misc` | 옛 글 보관 |
| `project` | `academic` `side` `disney_pop` | 프로젝트 소개 |

새 글은 `unreal` 이나 `fundamentals` 로 간다. `post` `archive` `project` 는 과거 글의 자리다.

## Step 2 — front matter

```markdown
---
title: "[Unreal] 제목"
classes: wide
categories:
  - unreal
  - framework
sidebar:
  nav: "main"
author_profile: true
---
```

**제목 접두사는 반드시 붙인다.** 사이트의 252편 전부가 갖고 있다.

| 접두사 | 언제 |
|---|---|
| `[DevNote]` | **실제로 작업한 프로젝트에서 겪은 일.** 문제 → 원인 → 해결 |
| `[Unreal]` | 엔진 문서·소스를 읽고 정리한 글 |
| `[C++]` `[C#]` `[Unity]` `[OS]` `[Network]` `[Math]` `[3D Graphics]` `[Design Pattern]` `[Game A.I.]` `[Misc]` | 주제별 |
| `[Project]` `[Academic]` | 프로젝트·학교 작업 소개 |

`[DevNote]` 와 `[Unreal]` 의 구분이 이 사이트에서 실무 경험을 가리키는 유일한 표시다. 엔진 공부 글에 `[DevNote]` 를 붙이면 그 표시가 아무 뜻도 갖지 못한다.

## Step 3 — 이미지

글 하나에 폴더 하나. 파일명은 글에 나오는 순서대로 번호를 매긴다.

```
assets/images/<글-slug>/01.png
assets/images/<글-slug>/02.gif
```

`<글-slug>` 는 파일명에서 날짜를 뗀 것이다 — `2025-08-12-SoftTarget.md` → `SoftTarget/`.

```markdown
![락온 대상 판정 범위](/assets/images/SoftTarget/01.png)
```

**alt 텍스트를 반드시 채운다.** 파일명이 번호라서 alt 가 그림의 뜻을 담는 유일한 자리다.

## Step 4 — 본문

- 코드블록에 언어 태그를 붙인다 — `c++` `csharp` `javascript` `bash` `yaml`. `c` `cs` `c#` `cpp` `js` 같은 별칭은 쓰지 않는다
- 코드 들여쓰기는 **2칸**. 탭은 쓰지 않는다 (`<pre>` 에서 8칸으로 벌어진다)
- 다른 글을 가리킬 때는 절대 URL 을 쓴다 — `https://jaykop.github.io/fundamentals/cpp/Casting/`
- 회사·프로젝트 코드네임을 쓰지 않는다. "우리 프로젝트" 같은 1인칭 소속 표현 대신 "해당 프로젝트" 로 쓴다

### DevNote 글의 뼈대

```markdown
## 상황
<!-- 무엇을 만들려다 무엇이 막혔나 -->

## 원인
<!-- 왜 그랬나. 엔진 쪽 동작을 짚는다 -->

## 해결
<!-- 어떻게 했나. 코드와 그림 -->

## 남은 것
<!-- 알면서 안 한 것, 나중에 볼 것 -->
```

## Step 5 — 점검

```bash
bundle exec jekyll build
python .claude/skills/devlog-check/devlog_check.py <새 글 경로>
```
