#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取 Flyway 增量 DDL 中的结构变更操作（CREATE TABLE / ALTER TABLE ADD / CREATE INDEX / DROP）。
用法： python3 extract_deltas.py <dir>
"""
import sys, os, re, glob

def extract(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    ops = []
    # CREATE TABLE
    for m in re.finditer(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`"]?([A-Za-z0-9_]+)', content, re.IGNORECASE):
        ops.append(('CREATE TABLE', m.group(1)))
    # ALTER TABLE ... ADD
    for m in re.finditer(r'ALTER\s+TABLE\s+[`"]?([A-Za-z0-9_]+)[`"]?\s+ADD\s+(?:COLUMN\s+)?[`"]?([A-Za-z0-9_]+)', content, re.IGNORECASE):
        ops.append(('ADD COLUMN', f"{m.group(1)}.{m.group(2)}"))
    # CREATE INDEX
    for m in re.finditer(r'CREATE\s+(?:UNIQUE\s+)?INDEX\s+[`"]?([A-Za-z0-9_]+)[`"]?\s+ON\s+[`"]?([A-Za-z0-9_]+)', content, re.IGNORECASE):
        ops.append(('CREATE INDEX', f"{m.group(2)} ({m.group(1)})"))
    # DROP
    for m in re.finditer(r'(DROP\s+TABLE\s+[`"]?[A-Za-z0-9_]+|DROP\s+COLUMN\s+[`"]?[A-Za-z0-9_]+)', content, re.IGNORECASE):
        ops.append(('DROP', m.group(1)))
    # ALTER TABLE ... MODIFY / CHANGE
    for m in re.finditer(r'ALTER\s+TABLE\s+[`"]?([A-Za-z0-9_]+)[`"]?\s+(MODIFY|CHANGE)\b', content, re.IGNORECASE):
        ops.append(('ALTER/MODIFY', m.group(1)))
    # INSERT (seed data)
    inserts = len(re.findall(r'\bINSERT\s+INTO\b', content, re.IGNORECASE))
    return ops, inserts

def main():
    d = sys.argv[1]
    files = sorted(glob.glob(os.path.join(d, 'V2*.sql')))
    for fp in files:
        ops, ins = extract(fp)
        print(f"\n### {os.path.basename(fp)}  (ops={len(ops)}, inserts={ins})")
        for kind, name in ops:
            print(f"  - {kind}: {name}")

if __name__ == '__main__':
    main()
