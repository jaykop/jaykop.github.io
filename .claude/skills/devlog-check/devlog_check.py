#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
devlog 글의 기계적 점검. 판단이 필요한 항목은 SKILL.md 가 맡는다.

  python devlog_check.py <file|dir> ...
  python devlog_check.py --all          # _posts + _pages 전체

확정 문제가 하나라도 있으면 exit 1.
"""
import os
import re
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
BOM = b"\xef\xbb\xbf"
OPT_OUT = "<!-- devlog-check: ignore -->"

# 코드블록에 허용하는 언어 태그. 별칭이 섞이면 하이라이팅이 갈린다.
LANG_OK = {"c++", "csharp", "javascript", "http", "bash", "yaml", "json",
           "text", "python", "glsl", "hlsl"}
LANG_FIX = {"c": "c++", "cpp": "c++", "cs": "csharp", "c#": "csharp",
            "js": "javascript"}

# 제목 접두사 — 사이트에서 실제로 쓰는 것만
PREFIX_OK = {"[C++]", "[C#]", "[C++/C#]", "[Unreal]", "[DevNote]", "[Unity]",
             "[Misc]", "[OS]", "[Network]", "[Math]", "[3D", "[Design",
             "[Game", "[Project]", "[Academic]"}

# 언리얼·게임 용어 표기 갈림
VARIANT_SETS = [
    ("나이아가라", "니아가라"),
    ("대미지", "데미지"),
    ("에셋", "애셋"),
    ("셰이더", "쉐이더"),
    ("셰이프", "쉐이프"),
    ("프레임레이트", "프레임 레이트"),
    ("리플리케이션", "레플리케이션"),
    ("머티리얼", "마테리얼"),
]

# 영어 관용구를 낱말째 옮긴 표현
BANNED = {
    "폴백": "대체 (에디터 필드명 Fallback 은 그대로)",
    "스테일": "낡음 / 갱신 안 됨",
    "센티넬": "잘못 넘어가는 걸 막는 장치",
    "냄새가 난": "나중에 문제가 될 것 같",
    "제품 코드": "실제 코드 (production code 직역)",
    "논리 구멍": "빠진 경우 / 규칙이 안 다루는 경우",
}
BANNED_SOFT = {
    "죽은 코드": "안 쓰이는 코드",
    "살아있": "동작 중 — 기능·코드가 주어일 때만. 캐릭터가 주어면 그대로",
}


def strip_code(t):
    """코드 펜스 · 인라인 코드 · HTML 주석은 검사에서 뺀다."""
    t = re.sub(r"^```.*?^```", "", t, flags=re.S | re.M)
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", t)


def slug(h):
    s = re.sub(r"[^\w\s가-힣-]", "", h.strip().lower())
    return re.sub(r"\s+", "-", s)


def fences(lines):
    """(lang, 0-based 여는 줄, 본문 줄들) 목록"""
    out, i = [], 0
    while i < len(lines):
        m = re.match(r"^\s*```([^\s`]*)\s*$", lines[i])
        if not m:
            i += 1
            continue
        lang, st, body = m.group(1), i, []
        i += 1
        while i < len(lines) and not re.match(r"^\s*```\s*$", lines[i]):
            body.append(lines[i])
            i += 1
        i += 1
        out.append((lang, st, body))
    return out


def check(path, site_urls):
    hard, soft = [], []
    raw = open(path, "rb").read()
    if raw.startswith(BOM):
        hard.append("BOM 이 있다 — BOM 없는 UTF-8 로 저장")
    # git 이 체크아웃할 때 CRLF 로 바꾸므로 정규화한 뒤 본다
    text = raw.decode("utf-8", "replace").replace("\r\n", "\n")
    if OPT_OUT in text:
        return [], []
    lines = text.split("\n")
    rel = os.path.relpath(path, ROOT).replace("\\", "/")
    is_post = rel.startswith("_posts/")

    # 파일이 --- 로 끝나고 개행이 없는 경우도 받는다
    fm = re.match(r"^---\n(.*?)\n---\s*?(?:\n|$)", text, re.S)
    if not fm:
        hard.append("front matter 가 없다")
        return hard, soft
    head = fm.group(1)

    title = re.search(r"^title:\s*(.*?)\s*$", head, re.M)
    if not title:
        hard.append("title 이 없다")
    elif is_post:
        val = title.group(1).strip().strip('"')
        first = val.split(" ")[0]
        if not val.startswith("["):
            hard.append("제목에 접두사가 없다 — " + val)
        elif first not in PREFIX_OK:
            hard.append("알 수 없는 제목 접두사 " + first
                        + " — 새 접두사면 PREFIX_OK 에 추가")

    if is_post:
        cats = re.search(r"^categories:\s*\n((?:\s*-\s*\S.*\n)+)", head, re.M)
        if not cats:
            hard.append("categories 가 없다")
        else:
            n = len([x for x in cats.group(1).strip().split("\n") if x.strip()])
            if n != 2:
                hard.append("categories 가 %d단계다 — 2단계여야 한다" % n)

    for lang, st, body in fences(lines):
        ln = st + 1
        if not lang:
            soft.append("L%d: 코드블록에 언어 태그가 없다" % ln)
        elif lang in LANG_FIX:
            hard.append("L%d: 언어 태그 %s -> %s 로 통일" % (ln, lang, LANG_FIX[lang]))
        elif lang not in LANG_OK:
            soft.append("L%d: 처음 보는 언어 태그 %s" % (ln, lang))
        if any(x.startswith("\t") for x in body):
            hard.append("L%d: 코드블록에 탭이 있다 — 2칸 공백으로" % ln)
        w = set()
        for x in body:
            if x.strip():
                n = len(x) - len(x.lstrip(" "))
                if n:
                    w.add(n)
        if w and min(w) >= 4 and all(v % 4 == 0 for v in w):
            soft.append("L%d: 4칸 들여쓰기 — 사이트 기준은 2칸" % ln)

    clean = strip_code(text)

    expect = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", os.path.basename(path)[:-3])
    for m in re.finditer(r"assets/images/([^\s\"')\]]+)", text):
        p = urllib.parse.unquote(m.group(1))
        if not os.path.exists(os.path.join(ROOT, "assets", "images", p)):
            hard.append("이미지가 없다 — assets/images/" + p)
        elif is_post and "/" not in p:
            hard.append("이미지가 글 폴더 밖에 있다 — assets/images/%s -> %s/ 로"
                        % (p, expect))
        elif is_post and p.split("/")[0] != expect:
            soft.append("이미지가 다른 글 폴더에 있다 — assets/images/%s (기대 %s/)"
                        % (p, expect))

    if site_urls is not None:
        for m in re.finditer(r"https?://jaykop\.github\.io([^)>\"'\s]*)", text):
            u = urllib.parse.unquote(m.group(1).split("#")[0])
            if not (u in site_urls or u.rstrip("/") in site_urls
                    or u + "/" in site_urls):
                hard.append("내부 링크가 깨졌다 — " + u)

    heads = set(slug(h) for h in re.findall(r"^#{1,6}\s+(.*)$", clean, re.M))
    for m in re.finditer(r"\]\(#([^)]+)\)", clean):
        if urllib.parse.unquote(m.group(1)) not in heads:
            hard.append("앵커가 제목과 안 맞는다 — #" + m.group(1))

    for w, alt in BANNED.items():
        if w in clean:
            hard.append("금지어 '%s' -> %s" % (w, alt))
    for w, alt in BANNED_SOFT.items():
        if w in clean:
            soft.append("확인 필요 '%s' -> %s" % (w, alt))
    for s in VARIANT_SETS:
        found = [v for v in s if v in clean]
        if len(found) > 1:
            hard.append("한 글 안에서 표기가 갈린다 — " + " / ".join(found))

    return hard, soft


def collect(args):
    out = []
    for a in args:
        if os.path.isdir(a):
            for r, d, fs in os.walk(a):
                out += [os.path.join(r, f) for f in fs if f.endswith(".md")]
        elif a.endswith(".md"):
            out.append(a)
    return sorted(out)


def main(argv):
    if "--all" in argv:
        targets = collect([os.path.join(ROOT, "_posts"),
                           os.path.join(ROOT, "_pages")])
    else:
        targets = collect([a for a in argv if not a.startswith("--")])
    if not targets:
        print("대상 파일이 없다. 경로나 --all 을 준다.")
        return 2

    site = os.path.join(ROOT, "_site")
    site_urls = None
    if os.path.isdir(site):
        site_urls = set()
        for r, d, fs in os.walk(site):
            for f in fs:
                p = os.path.relpath(os.path.join(r, f), site).replace("\\", "/")
                site_urls.add("/" + p)
                if f == "index.html":
                    dd = "/" + os.path.dirname(p).replace("\\", "/")
                    site_urls.add(dd)
                    site_urls.add(dd + "/")

    stray = []
    for r, d, fs in os.walk(os.path.join(ROOT, "_posts")):
        stray += [os.path.join(r, f) for f in fs if not f.endswith(".md")]

    nh = ns = 0
    for t in targets:
        h, s = check(t, site_urls)
        if h or s:
            print("\n" + os.path.relpath(t, ROOT).replace("\\", "/"))
            for x in h:
                print("  [문제] " + x)
            for x in s:
                print("  [참고] " + x)
        nh += len(h)
        ns += len(s)

    if stray:
        print("\n_posts 안에 확장자 없는 파일 — Jekyll 이 글로 인식하지 않는다."
              " 미완성이면 _drafts/ 로 옮긴다:")
        for p in stray:
            print("  [문제] " + os.path.relpath(p, ROOT).replace("\\", "/"))
        nh += len(stray)

    print("\n검사 %d개 · 문제 %d · 참고 %d" % (len(targets), nh, ns))
    return 1 if nh else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
