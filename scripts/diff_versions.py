#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DataEase Source Knowledge Base - 版本差异引擎

功能:
  对比 DataEase 两个版本之间的源码差异，为知识库「增量升级」提供量化依据。

  支持两种输入模式:
    A) 地图模式 (map-only):
       直接对比两份预先生成的 source-map.json (由 scan_source.py 产出)。
       通过 文件 size 差异判定 modified (快速，但无法区分「内容变但 size 不变」的情况)。

    B) 自动模式 (auto / git-ref):
       给定 --src (源码 git 仓库) 与 --old-ref / --new-ref (tag 或 commit)，
       内部用 `git ls-tree -r -l <ref>` 一次性取得每个文件的 blob-sha 与 size，
       以 sha 精确判定 added / removed / modified，无需 checkout，不污染工作区。

输出:
  metadata/diff-<old>..<new>.json
    - summary: 总数、增/删/改计数、按 module/language/category 聚合
    - added / removed / modified: 明细列表
    - unchangedCount: 未变化文件数

用法:
  # 模式 A: 对比两份地图
  python3 diff_versions.py \
      --old-map metadata/source-map.json \
      --new-map metadata/source-map-v2.10.8.json \
      --out   metadata/diff-v2.10.7..v2.10.8.json

  # 模式 B: 直接对两个 git 标签做差异
  python3 diff_versions.py \
      --src /path/to/dataease \
      --old-ref v2.10.7 --new-ref v2.10.8 \
      --out metadata/diff-v2.10.7..v2.10.8.json

依赖: 仅模式 B 需要源码目录为 git 仓库。
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

# 复用 scan_source.py 的分类与模块映射，保证与 source-map 口径一致
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import scan_source as ss
    MODULE_MAP = ss.MODULE_MAP
    LANG_MAP = ss.LANG_MAP
    CODE_LANGS = ss.CODE_LANGS
    classify = ss.classify
    map_module = ss.map_module
except Exception as e:  # pragma: no cover
    print(f"WARN: 无法复用 scan_source: {e}，使用内建降级逻辑", file=sys.stderr)
    MODULE_MAP = []
    LANG_MAP = {}
    CODE_LANGS = set()
    classify = lambda p, l: "other"
    map_module = lambda p: "root"


def _entry_from_map(obj):
    """从 source-map.json 的 files[] 元素构造统一 entry。"""
    return {
        "path": obj["path"],
        "module": obj.get("module") or map_module(obj["path"]),
        "language": obj.get("language") or LANG_MAP.get(os.path.splitext(obj["path"])[1].lower(), "other"),
        "category": obj.get("category") or classify(obj["path"], obj.get("language", "other")),
        "size": obj.get("size", 0),
        "loc": obj.get("loc"),
        "sha": None,  # 地图模式无 sha
    }


def _load_map(path):
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    files = data.get("files", [])
    version = data.get("version", "unknown")
    return version, {e["path"]: _entry_from_map(e) for e in files}


def _scan_ref(src, ref):
    """模式 B: 用 git ls-tree -r -l 取得 ref 下所有文件的 sha+size (不读内容, 不 checkout)。"""
    try:
        raw = subprocess.check_output(
            ["git", "-C", src, "ls-tree", "-r", "-l", ref], text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"ERROR: git ls-tree {ref} 失败: {e}", file=sys.stderr)
        sys.exit(1)

    result = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        # 格式: <mode> SP <type> SP <sha> SP <size> TAB <path>
        tab = line.find("\t")
        if tab < 0:
            continue
        meta = line[:tab].split()
        if len(meta) < 4:
            continue
        sha = meta[2]
        try:
            size = int(meta[3])
        except ValueError:
            size = 0
        path = line[tab + 1:]
        ext = os.path.splitext(path)[1].lower()
        lang = LANG_MAP.get(ext, "other")
        result[path] = {
            "path": path,
            "module": map_module(path),
            "language": lang,
            "category": classify(path, lang),
            "size": size,
            "loc": None,  # 自动模式不读内容, loc 留空
            "sha": sha,
        }
    return result


def _aggregate(entries, key):
    out = {}
    for e in entries:
        k = e[key]
        d = out.setdefault(k, {"total": 0, "source": 0, "loc": 0})
        d["total"] += 1
        if e["category"] == "source":
            d["source"] += 1
        if e.get("loc"):
            d["loc"] += e["loc"]
    return dict(sorted(out.items()))


def diff(old_map, new_map):
    """对比两个 path->entry 字典，返回完整 diff 结构。"""
    old_keys = set(old_map)
    new_keys = set(new_map)

    added_keys = new_keys - old_keys
    removed_keys = old_keys - new_keys
    common = old_keys & new_keys

    added, removed, modified = [], [], []
    unchanged = 0
    for p in common:
        o, n = old_map[p], new_map[p]
        # 优先用 sha；地图模式无 sha 时退化为 size
        if o.get("sha") is not None and n.get("sha") is not None:
            changed = o["sha"] != n["sha"]
        else:
            changed = o["size"] != n["size"]
        if changed:
            modified.append({
                "path": p,
                "module": n["module"],
                "language": n["language"],
                "category": n["category"],
                "oldSize": o["size"], "newSize": n["size"],
                "oldLoc": o.get("loc"), "newLoc": n.get("loc"),
                "oldSha": o.get("sha"), "newSha": n.get("sha"),
            })
        else:
            unchanged += 1

    for p in sorted(added_keys):
        e = new_map[p]
        added.append({k: e[k] for k in ("path", "module", "language", "category", "size", "loc", "sha")})
    for p in sorted(removed_keys):
        e = old_map[p]
        removed.append({k: e[k] for k in ("path", "module", "language", "category", "size", "loc", "sha")})

    method = "git-ls-tree+sha256" if any(e.get("sha") for e in new_map.values()) else "source-map-size"

    summary = {
        "totalOld": len(old_map),
        "totalNew": len(new_map),
        "added": len(added),
        "removed": len(removed),
        "modified": len(modified),
        "unchanged": unchanged,
        "byCategory": {
            "added": _aggregate(added, "category"),
            "removed": _aggregate(removed, "category"),
            "modified": _aggregate(modified, "category"),
        },
        "byModule": {
            "added": _aggregate(added, "module"),
            "removed": _aggregate(removed, "module"),
            "modified": _aggregate(modified, "module"),
        },
        "byLanguage": {
            "added": _aggregate(added, "language"),
            "removed": _aggregate(removed, "language"),
            "modified": _aggregate(modified, "language"),
        },
    }

    return {
        "project": "DataEase",
        "method": method,
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "summary": summary,
        "added": added,
        "removed": removed,
        "modified": modified,
        "unchangedCount": unchanged,
    }


def main():
    ap = argparse.ArgumentParser()
    # 模式 A
    ap.add_argument("--old-map", help="旧版本 source-map.json")
    ap.add_argument("--new-map", help="新版本 source-map.json")
    ap.add_argument("--old-version", help="旧版本标签(仅用于输出标注)")
    ap.add_argument("--new-version", help="新版本标签(仅用于输出标注)")
    # 模式 B
    ap.add_argument("--src", help="源码 git 仓库根目录")
    ap.add_argument("--old-ref", help="旧版本 git ref (tag/commit)")
    ap.add_argument("--new-ref", help="新版本 git ref (tag/commit)")
    # 通用
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "metadata", "diff.json"))
    args = ap.parse_args()

    out = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)

    # 解析旧版本
    if args.old_map:
        ov, old_map = _load_map(os.path.abspath(args.old_map))
    elif args.src and args.old_ref:
        ov = args.old_ref
        old_map = _scan_ref(os.path.abspath(os.path.expanduser(args.src)), args.old_ref)
    else:
        print("ERROR: 需提供 --old-map 或 (--src + --old-ref)", file=sys.stderr)
        sys.exit(1)

    # 解析新版本
    if args.new_map:
        nv, new_map = _load_map(os.path.abspath(args.new_map))
    elif args.src and args.new_ref:
        nv = args.new_ref
        new_map = _scan_ref(os.path.abspath(os.path.expanduser(args.src)), args.new_ref)
    else:
        print("ERROR: 需提供 --new-map 或 (--src + --new-ref)", file=sys.stderr)
        sys.exit(1)

    ov = args.old_version or ov
    nv = args.new_version or nv

    result = diff(old_map, new_map)
    result["oldVersion"] = ov
    result["newVersion"] = nv

    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)

    s = result["summary"]
    print(f"OK diff -> {out}")
    print(f"    {ov} -> {nv}  (method: {result['method']})")
    print(f"    total: {s['totalOld']} -> {s['totalNew']}")
    print(f"    added:{s['added']}  removed:{s['removed']}  modified:{s['modified']}  unchanged:{s['unchanged']}")
    # 按类别打印 modified 分布
    mod_by_cat = s["byCategory"]["modified"]
    if mod_by_cat:
        print("    modified by category:")
        for cat, d in mod_by_cat.items():
            print(f"      {cat:10s} {d['total']}")


if __name__ == "__main__":
    main()
