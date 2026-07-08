#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 parse_ddl 的文本输出转换为 Markdown 表格（每张表一个表）。
输入： parse_ddl.py 的输出文件
输出： markdown 表（按原顺序）
"""
import sys, re

def parse_file(path):
    tables = []
    cur = None
    with open(path) as f:
        for line in f:
            m = re.match(r'^## (\S+)  \(([0-9]+) cols\)(.*)$', line)
            if m:
                if cur: tables.append(cur)
                cur = {'name': m.group(1), 'n': int(m.group(2)), 'extra': m.group(3).strip(), 'cols': []}
                continue
            cm = re.match(r'\s*- ([A-Za-z0-9_]+): (.+)$', line)
            if cm and cur:
                cur['cols'].append(cm.group(1) + ': ' + cm.group(2))
    if cur: tables.append(cur)
    return tables

def col_to_md(colstr):
    # colstr like "name: varchar(255) [NN] -- 注释"
    name, rest = colstr.split(': ', 1)
    nn = ' [NN]' in rest
    rest = rest.replace(' [NN]', '')
    default = None
    dm = re.search(r' default=([^\s]+)', rest)
    if dm:
        default = dm.group(1); rest = rest.replace(dm.group(0), '')
    comment = None
    cmt = re.search(r' -- (.+)$', rest)
    if cmt:
        comment = cmt.group(1); rest = rest.replace(cmt.group(0), '')
    ctype = rest.strip()
    flags = 'NOT NULL' if nn else 'NULL'
    dval = default if default else ''
    cmtval = comment if comment else ''
    return f"| `{name}` | `{ctype}` | {flags} | {dval} | {cmtval} |"

def main():
    tables = parse_file(sys.argv[1])
    out = []
    for t in tables:
        out.append(f"\n### {t['name']}  （{t['n']} 列{t['extra']}）\n")
        out.append("| 列 | 类型 | 空 | 默认 | 说明 |")
        out.append("|----|------|----|------|------|")
        for c in t['cols']:
            out.append(col_to_md(c))
    print('\n'.join(out))

if __name__ == '__main__':
    main()
