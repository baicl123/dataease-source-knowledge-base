#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DataEase DDL 解析器 v2
解析 MySQL DDL（CREATE TABLE），正确处理嵌套括号与多行类型。
用法： python3 parse_ddl.py <file.sql>
"""
import sys
import re

def find_table_blocks(content):
    """返回 list of (table_name, body_str)"""
    blocks = []
    # 找 CREATE TABLE 起始
    for m in re.finditer(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`"]?([A-Za-z0-9_]+)[`"]?\s*\(', content, re.IGNORECASE):
        name = m.group(1)
        start = m.end() - 1  # 指向 '('
        depth = 0
        i = start
        n = len(content)
        while i < n:
            ch = content[i]
            if ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
                if depth == 0:
                    body = content[start+1:i]
                    blocks.append((name, body))
                    break
            i += 1
    return blocks

def split_top_level(body):
    """按顶层逗号切分（忽略括号内的逗号）"""
    parts = []
    depth = 0
    cur = ''
    for ch in body:
        if ch == '(':
            depth += 1
            cur += ch
        elif ch == ')':
            depth -= 1
            cur += ch
        elif ch == ',' and depth == 0:
            parts.append(cur)
            cur = ''
        else:
            cur += ch
    if cur.strip():
        parts.append(cur)
    return parts

def parse_columns(parts):
    cols = []
    constraints = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        up = p.upper()
        if re.match(r'(PRIMARY\s+KEY|KEY|INDEX|UNIQUE|CONSTRAINT|FOREIGN|CHECK)', up):
            constraints.append(p)
            continue
        cm = re.match(r'[`"]?([A-Za-z0-9_]+)[`"]?\s+([A-Za-z0-9_]+(?:\s*\([^)]*\))?)', p)
        if not cm:
            # 可能是无引号或特殊类型，记录原始
            continue
        col = cm.group(1)
        ctype = re.sub(r'\s+', ' ', cm.group(2))
        nullable = 'NOT NULL' not in up
        default = None
        dm = re.search(r"DEFAULT\s+(NULL|'[^']*'|[0-9A-Za-z_.\-]+)", p, re.IGNORECASE)
        if dm:
            default = dm.group(1)
        comment = None
        cmt = re.search(r"COMMENT\s+'([^']*)'", p, re.IGNORECASE)
        if cmt:
            comment = cmt.group(1)
        cols.append({'name': col, 'type': ctype, 'nullable': nullable,
                     'default': default, 'comment': comment})
    return cols, constraints

def parse_ddl(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    out = []
    for name, body in find_table_blocks(content):
        parts = split_top_level(body)
        cols, constraints = parse_columns(parts)
        out.append({'name': name, 'columns': cols, 'constraints': constraints})
    return out

def main():
    if len(sys.argv) < 2:
        print("usage: parse_ddl.py <file.sql>")
        sys.exit(1)
    tables = parse_ddl(sys.argv[1])
    for t in tables:
        print(f"\n## {t['name']}  ({len(t['columns'])} cols)")
        for c in t['columns']:
            nn = '' if c['nullable'] else ' [NN]'
            d = f" default={c['default']}" if c['default'] else ''
            ct = f" -- {c['comment']}" if c['comment'] else ''
            print(f"  - {c['name']}: {c['type']}{nn}{d}{ct}")

if __name__ == '__main__':
    main()
