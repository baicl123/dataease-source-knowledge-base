#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DataEase Source Knowledge Base - 源码扫描器

功能:
  1. 通过 `git ls-files` 获取权威文件清单 (排除未跟踪/忽略文件)
  2. 按 Maven 模块 / 顶层目录归类
  3. 按扩展名识别语言与类别 (source / config / asset / data / doc / build)
  4. 计算文件大小与代码行数 (LOC)
  5. 输出 source-map.json 与 statistics.json 到 ../metadata/

用法:
  python3 scan_source.py [--src <源码根目录>] [--out <metadata 目录>] [--version v2.10.7]

依赖: 仅在源码根目录有 .git 时运行 (使用 git ls-files)。
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

# ---- Maven 模块映射 (目录前缀 -> 模块名) ----
MODULE_MAP = [
    ("core/core-backend/", "core-backend"),
    ("core/core-frontend/", "core-frontend"),
    ("sdk/api/api-base/", "sdk-api-base"),
    ("sdk/api/api-permissions/", "sdk-api-permissions"),
    ("sdk/api/api-sync/", "sdk-api-sync"),
    ("sdk/common/", "sdk-common"),
    ("sdk/distributed/", "sdk-distributed"),
    ("sdk/extensions/extensions-datafilling/", "sdk-ext-datafilling"),
    ("sdk/extensions/extensions-datasource/", "sdk-ext-datasource"),
    ("sdk/extensions/extensions-view/", "sdk-ext-view"),
    ("drivers/", "drivers"),
    ("installer/", "installer"),
    ("mapFiles/", "mapFiles"),
    ("staticResource/", "staticResource"),
    (".github/", "github-ci"),
    ("docs/", "dataease-docs"),
]

# 非源码根目录 (不计入 source 覆盖率统计, 但仍登记到文件清单)
NON_SOURCE_PREFIXES = ("mapFiles/", "staticResource/", "drivers/", ".github/", "docs/")

# 语言映射
LANG_MAP = {
    ".java": "java",
    ".vue": "vue",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".sql": "sql",
    ".xml": "xml",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".json": "json",
    ".css": "stylesheet",
    ".less": "stylesheet",
    ".scss": "stylesheet",
    ".svg": "svg",
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
    ".gif": "image",
    ".woff": "font",
    ".woff2": "font",
    ".ttf": "font",
    ".md": "markdown",
    ".sh": "shell",
    ".properties": "properties",
    ".env": "env",
    ".toml": "toml",
    ".lua": "lua",
    ".html": "html",
    ".stg": "stringtemplate",
    ".service": "systemd",
    ".jar": "jar",
    ".gitkeep": "gitkeep",
    ".editorconfig": "config",
    ".gitignore": "config",
    ".gitattributes": "config",
    ".npmrc": "config",
    ".prettierignore": "config",
    ".eslintignore": "config",
    ".gitmodules": "config",
    ".typos.toml": "toml",
}

# 代码类语言 (计入 LOC 与 source 覆盖率)
CODE_LANGS = {"java", "vue", "typescript", "javascript", "sql", "xml", "yaml", "properties", "shell", "lua", "html", "stringtemplate", "toml"}

# 类别判定
def classify(path: str, lang: str) -> str:
    base = os.path.basename(path)
    if path.startswith(NON_SOURCE_PREFIXES):
        if lang in ("image", "font", "svg"):
            return "asset"
        if lang == "json":
            return "data"
        return "data"
    if lang in CODE_LANGS:
        if lang == "sql":
            return "source"
        if base == "pom.xml":
            return "build"
        if lang in ("yaml", "properties", "toml", "env") and (
            "application" in base or "bootstrap" in base or base.endswith(".properties") or base.endswith(".env") or base.endswith(".toml")
        ):
            return "config"
        if lang in ("yaml", "properties", "toml", "env"):
            return "config"
        return "source"
    if lang == "json":
        if base in ("package.json", "tsconfig.json", "vue.config.js", "babel.config.js", "vite.config.ts"):
            return "build"
        return "config"
    if lang in ("image", "font", "svg"):
        return "asset"
    if lang == "markdown":
        return "doc"
    if lang in ("shell", "systemd", "jar", "gitkeep", "config"):
        return "build" if lang in ("shell", "systemd", "jar") else "config"
    return "other"


def map_module(path: str) -> str:
    for prefix, mod in MODULE_MAP:
        if path.startswith(prefix):
            return mod
    return "root"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=os.environ.get("DATAEASE_SRC", "~/workspace/code/references/dataease"))
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "metadata"))
    ap.add_argument("--version", default="v2.10.7")
    args = ap.parse_args()

    src = os.path.abspath(os.path.expanduser(args.src))
    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)

    if not os.path.isdir(os.path.join(src, ".git")):
        print(f"ERROR: {src} 不是 git 仓库 (缺少 .git)", file=sys.stderr)
        sys.exit(1)

    # 获取 git ls-files
    try:
        files_raw = subprocess.check_output(
            ["git", "-C", src, "ls-files"], text=True
        ).splitlines()
    except subprocess.CalledProcessError as e:
        print(f"ERROR: git ls-files 失败: {e}", file=sys.stderr)
        sys.exit(1)

    files = []
    by_module = {}
    by_lang = {}
    by_category = {}
    source_file_count = 0

    for rel in files_raw:
        if not rel:
            continue
        full = os.path.join(src, rel)
        ext = os.path.splitext(rel)[1].lower()
        lang = LANG_MAP.get(ext, "other")
        module = map_module(rel)
        category = classify(rel, lang)
        try:
            size = os.path.getsize(full)
        except OSError:
            size = 0
        loc = None
        if lang in CODE_LANGS and os.path.isfile(full):
            try:
                with open(full, "rb") as fh:
                    loc = sum(1 for _ in fh)
            except OSError:
                loc = 0
        is_source = (category == "source")
        if is_source:
            source_file_count += 1

        entry = {
            "path": rel,
            "module": module,
            "language": lang,
            "category": category,
            "size": size,
            "loc": loc,
            "source": is_source,
        }
        files.append(entry)

        by_module.setdefault(module, {"total": 0, "source": 0, "loc": 0})
        by_module[module]["total"] += 1
        if is_source:
            by_module[module]["source"] += 1
        if loc:
            by_module[module]["loc"] += loc

        by_lang.setdefault(lang, {"total": 0, "source": 0, "loc": 0})
        by_lang[lang]["total"] += 1
        if is_source:
            by_lang[lang]["source"] += 1
        if loc:
            by_lang[lang]["loc"] += loc

        by_category.setdefault(category, 0)
        by_category[category] += 1

    # 文件按路径排序
    files.sort(key=lambda f: f["path"])

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    source_map = {
        "project": "DataEase",
        "version": args.version,
        "generatedAt": generated_at,
        "sourcePath": src,
        "method": "git ls-files",
        "summary": {
            "totalFiles": len(files),
            "sourceFiles": source_file_count,
            "totalLoc": sum((f["loc"] or 0) for f in files),
            "byModule": {k: v for k, v in sorted(by_module.items())},
            "byLanguage": {k: v for k, v in sorted(by_lang.items())},
            "byCategory": dict(sorted(by_category.items())),
        },
        "modules": {
            "core-backend": {"path": "core/core-backend", "type": "maven-module", "pom": "core/core-backend/pom.xml"},
            "core-frontend": {"path": "core/core-frontend", "type": "frontend(vue)", "pom": "core/core-frontend/pom.xml"},
            "sdk-api-base": {"path": "sdk/api/api-base", "type": "maven-module", "pom": "sdk/api/api-base/pom.xml"},
            "sdk-api-permissions": {"path": "sdk/api/api-permissions", "type": "maven-module", "pom": "sdk/api/api-permissions/pom.xml"},
            "sdk-api-sync": {"path": "sdk/api/api-sync", "type": "maven-module", "pom": "sdk/api/api-sync/pom.xml"},
            "sdk-common": {"path": "sdk/common", "type": "maven-module", "pom": "sdk/common/pom.xml"},
            "sdk-distributed": {"path": "sdk/distributed", "type": "maven-module", "pom": "sdk/distributed/pom.xml"},
            "sdk-ext-datafilling": {"path": "sdk/extensions/extensions-datafilling", "type": "maven-module", "pom": "sdk/extensions/extensions-datafilling/pom.xml"},
            "sdk-ext-datasource": {"path": "sdk/extensions/extensions-datasource", "type": "maven-module", "pom": "sdk/extensions/extensions-datasource/pom.xml"},
            "sdk-ext-view": {"path": "sdk/extensions/extensions-view", "type": "maven-module", "pom": "sdk/extensions/extensions-view/pom.xml"},
            "drivers": {"path": "drivers", "type": "jdbc-drivers(binary)"},
            "installer": {"path": "installer", "type": "deploy-scripts"},
            "mapFiles": {"path": "mapFiles", "type": "map-data(geojson/svg)"},
            "staticResource": {"path": "staticResource", "type": "static-assets"},
            "github-ci": {"path": ".github", "type": "ci-config"},
            "dataease-docs": {"path": "docs", "type": "upstream-docs"},
            "root": {"path": ".", "type": "repo-root"},
        },
        "files": files,
    }

    statistics = {
        "project": "DataEase",
        "version": args.version,
        "generatedAt": generated_at,
        "totals": {
            "files": len(files),
            "sourceFiles": source_file_count,
            "loc": sum((f["loc"] or 0) for f in files),
            "sourceLoc": sum((f["loc"] or 0) for f in files if f["source"]),
        },
        "byModule": source_map["summary"]["byModule"],
        "byLanguage": source_map["summary"]["byLanguage"],
        "byCategory": source_map["summary"]["byCategory"],
        "mavenModules": [m for m, v in source_map["modules"].items() if v.get("type", "").startswith("maven")],
    }

    sm_path = os.path.join(out, "source-map.json")
    st_path = os.path.join(out, "statistics.json")
    with open(sm_path, "w", encoding="utf-8") as fh:
        json.dump(source_map, fh, ensure_ascii=False, indent=2)
    with open(st_path, "w", encoding="utf-8") as fh:
        json.dump(statistics, fh, ensure_ascii=False, indent=2)

    print(f"OK source-map.json  -> {sm_path}")
    print(f"OK statistics.json  -> {st_path}")
    print(f"    total files : {len(files)}")
    print(f"    source files: {source_file_count}")
    print(f"    total LOC   : {statistics['totals']['loc']}")
    print(f"    source LOC  : {statistics['totals']['sourceLoc']}")


if __name__ == "__main__":
    main()
