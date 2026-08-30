#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
jaykop.github.io 구조 개편 마이그레이션
  기본은 dry-run. 실제 적용은 --apply
  롤백:  git checkout . && git clean -fd
"""
import csv, os, re, sys, shutil, subprocess, argparse

CAT_DIR = {
    "unreal|combat":    "_posts/unreal/combat",
    "unreal|character": "_posts/unreal/character",
    "unreal|camera":    "_posts/unreal/camera",
    "unreal|ai":        "_posts/unreal/ai",
    "unreal|perf":      "_posts/unreal/perf",
    "unreal|framework": "_posts/unreal/framework",
    "archive|game-ai-theory": "_posts/archive/game-ai-theory",
    "writing|cpp":            "_posts/writing/cpp",
    "writing|graphics":       "_posts/writing/graphics",
    "writing|design-pattern": "_posts/writing/design-pattern",
    "post|Unity":  "_posts/post/unity",
    "post|CSharp": "_posts/post/CSharp",
}
SYMBOLS = [
    ("ACampActor", "ACheckpointActor"),
    ("UAAALSLinkedAnimLayerInstance", "UCustomALSLinkedAnimLayerInstance"),
    ("FBTEnemyMasterServiceMemory", "FBTEnemyServiceMemory"),
]
RENAMES = {
    "_posts/post/unity/2021-03-04-frame debugger": "_posts/post/unity/2021-03-04-FrameDebugger.md",
    "_posts/post/unity/2021-04-12-animation":      "_posts/post/unity/2021-04-12-Animation.md",
    "_posts/post/CPP/2021-08-04-std_function":     "_posts/post/CPP/2021-08-04-std_function.md",
}
FM_CAT  = re.compile(r"^categories:[ \t]*\n(?:[ \t]*-[ \t]*\S.*\n)+", re.M)
FM_FEAT = re.compile(r"^featured:.*\n", re.M)

def rewrite_categories(text, cats):
    block = "categories:\n" + "".join(f"  - {c}\n" for c in cats.split("|"))
    if FM_CAT.search(text):
        return FM_CAT.sub(block, text, count=1)
    return re.sub(r"^---\n", "---\n" + block, text, count=1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="실제 적용 (기본은 dry-run)")
    ap.add_argument("--root", default=".", help="저장소 루트")
    ap.add_argument("--mapping", default="mapping.csv")
    a = ap.parse_args()
    os.chdir(a.root)
    if not os.path.isdir("_posts"):
        sys.exit("ERROR: _posts 가 없습니다. --root 로 저장소 루트를 지정하세요.")

    rows = list(csv.DictReader(open(a.mapping, encoding="utf-8")))
    log, missing, sym_hits = [], [], []

    for r in rows:
        old, act, cats = r["old_path"], r["action"], r["new_categories"]
        if not os.path.exists(old):
            missing.append(old); continue

        if act == "delete":
            log.append(("DEL ", old, ""))
            if a.apply: os.remove(old)

        elif act == "draft":
            dst = os.path.join("_drafts", os.path.basename(old))
            log.append(("DRAFT", old, dst))
            if a.apply:
                os.makedirs("_drafts", exist_ok=True); shutil.move(old, dst)

        elif act == "rename":
            dst = RENAMES[old]
            log.append(("REN ", old, dst))
            if a.apply: shutil.move(old, dst)

        elif act == "remap":
            d = CAT_DIR[cats]
            dst = os.path.join(d, os.path.basename(old))
            t = open(old, encoding="utf-8").read()
            t2 = rewrite_categories(t, cats)
            if r.get("featured") == "true":
                t2 = FM_FEAT.sub("", t2)
                t2 = re.sub(r"^(categories:\n(?:  - .*\n)+)", r"\1featured: true\n", t2, count=1, flags=re.M)
            for s, rep in SYMBOLS:
                if s in t2:
                    sym_hits.append((os.path.basename(old), s, rep))
                    t2 = t2.replace(s, rep)
            log.append(("MAP ", old, dst + f"   [{cats.replace('|',' / ')}]"))
            if a.apply:
                os.makedirs(d, exist_ok=True)
                open(dst, "w", encoding="utf-8").write(t2)
                if dst != old: os.remove(old)

    # 빈 디렉토리 정리
    if a.apply:
        for d in ["_posts/post/unreal","_posts/post/game_ai","_posts/project/project_aa",
                  "_posts/project/project_o","_posts/ready2post",
                  "_posts/post/CPP","_posts/post/graphics","_posts/post/design_pattern"]:
            if os.path.isdir(d) and not os.listdir(d): os.rmdir(d)
        for d in ["_posts/project"]:
            if os.path.isdir(d) and not os.listdir(d): os.rmdir(d)

    w = max((len(x[1]) for x in log), default=10)
    for k, s, d in log:
        print(f"  {k} {s:<{w}}  {'→ ' + d if d else ''}")
    print(f"\n총 {len(log)}건" + ("  [APPLIED]" if a.apply else "  [DRY-RUN — 적용하려면 --apply]"))
    if sym_hits:
        print("\n심볼 치환:")
        for f, s, r in sym_hits: print(f"  {f}: {s} → {r}")
    if missing:
        print("\n경로 없음 (확인 필요):")
        for m in missing: print("  " + m)

if __name__ == "__main__":
    main()
