#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聚合所有 migration DDL 中出现的 CREATE TABLE，输出完整 schema（按表去重）。
同时输出每个文件新增的 ADD COLUMN / CREATE INDEX / CREATE TABLE。
用法： python3 aggregate_schema.py <migration_dir>
"""
import sys, os, re, glob

def find_table_blocks(content):
    blocks = []
    for m in re.finditer(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`"]?([A-Za-z0-9_]+)[`"]?\s*\(', content, re.IGNORECASE):
        name = m.group(1)
        start = m.end() - 1
        depth = 0; i = start; n = len(content)
        while i < n:
            ch = content[i]
            if ch == '(': depth += 1
            elif ch == ')':
                depth -= 1
                if depth == 0:
                    blocks.append((name, content[start+1:i])); break
            i += 1
    return blocks

def split_top_level(body):
    parts=[]; depth=0; cur=''
    for ch in body:
        if ch=='(': depth+=1; cur+=ch
        elif ch==')': depth-=1; cur+=ch
        elif ch==',' and depth==0: parts.append(cur); cur=''
        else: cur+=ch
    if cur.strip(): parts.append(cur)
    return parts

def parse_columns(parts):
    cols=[]
    for p in parts:
        p=p.strip()
        if not p: continue
        if re.match(r'(PRIMARY\s+KEY|KEY|INDEX|UNIQUE|CONSTRAINT|FOREIGN|CHECK)', p.upper()): continue
        cm=re.match(r'[`"]?([A-Za-z0-9_]+)[`"]?\s+([A-Za-z0-9_]+(?:\s*\([^)]*\))?)', p)
        if not cm: continue
        col=cm.group(1); ctype=re.sub(r'\s+',' ',cm.group(2))
        nullable='NOT NULL' not in p.upper()
        default=None
        dm=re.search(r"DEFAULT\s+(NULL|'[^']*'|[0-9A-Za-z_.\-]+)", p, re.IGNORECASE)
        if dm: default=dm.group(1)
        comment=None
        cmt=re.search(r"COMMENT\s+'([^']*)'", p, re.IGNORECASE)
        if cmt: comment=cmt.group(1)
        cols.append({'name':col,'type':ctype,'nullable':nullable,'default':default,'comment':comment})
    return cols

def main():
    d=sys.argv[1]
    files=sorted(glob.glob(os.path.join(d,'V2*.sql')))
    all_tables={}
    table_origin={}
    for fp in files:
        with open(fp,'r',encoding='utf-8',errors='ignore') as f: content=f.read()
        for name,body in find_table_blocks(content):
            if name not in all_tables:
                all_tables[name]=parse_columns(split_top_level(body))
                table_origin[name]=os.path.basename(fp)
    print(f"TOTAL TABLES: {len(all_tables)}\n")
    for name in sorted(all_tables):
        cols=all_tables[name]
        print(f"## {name}  ({len(cols)} cols)  [from {table_origin[name]}]")
        for c in cols:
            nn='' if c['nullable'] else ' [NN]'
            dfl=f" default={c['default']}" if c['default'] else ''
            ct=f" -- {c['comment']}" if c['comment'] else ''
            print(f"  - {c['name']}: {c['type']}{nn}{dfl}{ct}")

if __name__=='__main__':
    main()
