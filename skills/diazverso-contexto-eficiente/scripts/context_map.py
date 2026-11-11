#!/usr/bin/env python3
"""Incremental local dependency graph for bounded retrieval; no network or model calls."""
from __future__ import annotations
import argparse
import ast
import hashlib
import importlib.util
import json
import math
import os
import re
import tempfile
import unicodedata
from pathlib import Path

VERSION = 2
EXTENSIONS = {'.md','.py','.json','.yaml','.yml','.ts','.tsx','.js','.mjs','.mts'}
SKIP = {'node_modules','__pycache__','.git','.venv','dist','build','out','tests'}
CATALOG = 'skills/diazverso-contexto-eficiente/references/skill-map.json'
PATH = re.compile(r'(?<![\w./-])((?:\.\./|\./)?(?:[\w.-]+/)+[\w.-]+\.(?:md|py|json|yaml|yml|ts|tsx|js|mjs|mts|png|wav))')
MAX_BYTES = 250_000
_route_spec=importlib.util.spec_from_file_location('diazverso_route',Path(__file__).with_name('route_request.py'))
_router=importlib.util.module_from_spec(_route_spec);_route_spec.loader.exec_module(_router)


def normalize(text: str) -> str:
    value=''.join(c for c in unicodedata.normalize('NFKD',text.casefold()) if not unicodedata.combining(c))
    aliases={'descricoes':'descricao','description':'descricao','descriptions':'descricao',
             'videos':'video','roteiros':'roteiro','scripts':'script','skills':'skill',
             'fontes':'fonte','sources':'fonte','legendas':'legenda','captions':'legenda',
             'miniatura':'thumbnail','miniaturas':'thumbnail','revisar':'review',
             'revisao':'review','revisoes':'review','reviewing':'review'}
    return re.sub(r'\b\w+\b',lambda m:aliases.get(m.group(),m.group()),value)


def safe_files(root: Path) -> list[Path]:
    found = [root/'plugin.json',root/'assets/manifest.json']
    for name in ('skills','schemas','templates'):
        anchor=root/name
        if anchor.is_dir() and not anchor.is_symlink():
            found.extend(p for p in anchor.rglob('*') if p.is_file())
    return sorted(set(p for p in found if p.is_file() and not p.is_symlink()
        and p.resolve().is_relative_to(root) and p.suffix in EXTENSIONS
        and p.relative_to(root).as_posix()!=CATALOG
        and not any(part in SKIP or part.startswith('.') for part in p.relative_to(root).parts)
        and p.name not in {'credentials.json','secret.json'} and p.stat().st_size<=MAX_BYTES))


def parse_node(root: Path, file: Path, content: str, stamp: list[int]) -> dict:
    lines=content.splitlines()
    headings=[{'line':i,'text':line.lstrip('# ').strip()[:120]}
              for i,line in enumerate(lines,1) if line.startswith(('# ','## '))][:10]
    description=next((line.partition(':')[2].strip().strip('"\'')[:300]
                      for line in lines[:15] if line.startswith('description:')),'')
    refs={}
    symbols=[]
    for number,line in enumerate(lines,1):
        for hit in PATH.finditer(line):
            target=hit.group(1)
            for candidate in (file.parent/target,root/target):
                dest=candidate.resolve()
                if dest.is_relative_to(root) and dest.is_file() and not candidate.is_symlink():
                    rel=dest.relative_to(root).as_posix()
                    refs.setdefault(rel,{'target':rel,'line':number})
                    break
    if file.suffix=='.py':
        try:
            tree=ast.parse(content)
            if not description:description=(ast.get_docstring(tree) or '').split('\n\n')[0][:300]
            symbols=[{'name':node.name,'line':node.lineno} for node in tree.body
                     if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))][:32]
            for node in ast.walk(tree):
                modules=([node.module] if isinstance(node,ast.ImportFrom) and node.module else
                         [a.name for a in node.names] if isinstance(node,ast.Import) else [])
                for module in modules:
                    dest=(file.parent/(module.replace('.','/')+'.py')).resolve()
                    if dest.is_relative_to(root) and dest.is_file():
                        rel=dest.relative_to(root).as_posix();refs.setdefault(rel,{'target':rel,'line':node.lineno})
        except SyntaxError:pass
    elif file.suffix in {'.js','.mjs','.ts','.tsx','.mts'}:
        symbols=[{'name':match.group(1),'line':content[:match.start()].count('\n')+1}
                 for match in re.finditer(r'export\s+(?:async\s+)?(?:function|const|class|type)\s+(\w+)',content)][:32]
    return {'sha256':hashlib.sha256(content.encode()).hexdigest(),'stamp':stamp,
            'title':headings[0]['text'] if headings else file.stem,
            'description':description,'headings':headings,'symbols':symbols,'references':list(refs.values())}


def build(root: Path, previous: dict | None = None) -> dict:
    root=root.resolve()
    root_key=hashlib.sha256(str(root).encode()).hexdigest()[:20]
    previous=previous if isinstance(previous,dict) else {}
    old=previous.get('nodes',{}) if previous.get('schema_version')==VERSION and previous.get('root_key')==root_key else {}
    if not isinstance(old,dict):old={}
    nodes={};parsed=reused=0
    for file in safe_files(root):
        rel=file.relative_to(root).as_posix();stat=file.stat()
        stamp=[stat.st_size,stat.st_mtime_ns,stat.st_ctime_ns]
        cached=old.get(rel)
        valid=(isinstance(cached,dict) and cached.get('stamp')==stamp
               and isinstance(cached.get('title'),str) and isinstance(cached.get('description'),str)
               and isinstance(cached.get('sha256'),str) and re.fullmatch(r'[a-f0-9]{64}',cached['sha256'])
               and isinstance(cached.get('headings'),list) and isinstance(cached.get('references'),list)
               and isinstance(cached.get('symbols'),list)
               and all(isinstance(symbol,dict) and isinstance(symbol.get('name'),str) for symbol in cached['symbols'])
               and all(isinstance(h,dict) and isinstance(h.get('text'),str) for h in cached['headings'])
               and all(isinstance(ref,dict) and isinstance(ref.get('target'),str) for ref in cached['references']))
        if valid:
            nodes[rel]=cached;reused+=1
        else:
            nodes[rel]=parse_node(root,file,file.read_bytes().decode('utf-8'),stamp);parsed+=1
    return {'schema_version':VERSION,'root_key':root_key,'nodes':nodes,
            'stats':{'files':len(nodes),'parsed':parsed,'reused':reused,'removed':len(set(old)-set(nodes))}}


def find(graph: dict, query: str, limit: int = 3) -> list[dict]:
    stop={'de','do','da','dos','das','um','uma','para','com','no','na','ao','os','as','em','que'}
    terms=[t for t in re.findall(r'[\w-]+',normalize(query)) if len(t)>1 and t not in stop]
    if not terms:return []
    ranked=[]
    haystacks={path:normalize(' '.join([path,node['title'],node['description']]+[h['text'] for h in node['headings']]+[s['name'] for s in node.get('symbols',[])]))
                for path,node in graph['nodes'].items()}
    weights={t:1+math.log((len(haystacks)+1)/(1+sum(t in text for text in haystacks.values()))) for t in terms}
    principal=_router.route(query).get('primary_skill')
    for path,node in graph['nodes'].items():
        haystack=haystacks[path]
        matched=[t for t in terms if t in haystack]
        score=sum(weights[t]*(3 if t in normalize(path) else 1) for t in matched)
        if path.endswith('/SKILL.md'):
            score*=1.3
            if normalize(path.split('/')[1]).removeprefix('diazverso-') in terms:score+=10
            if principal and path==f'skills/{principal}/SKILL.md':score+=10*sum(weights.values())
        if score:
            ranked.append((score,path,{'path':path,'title':node['title'],
                'description':node['description'],'sha256':node['sha256'],
                'matched_terms':matched,
                'headings':node['headings'][:3],
                'symbols':[s for s in node.get('symbols',[]) if any(t in normalize(s['name']) for t in terms)][:4],
                'references':[r for r in node['references'] if r['target'] in graph['nodes']][:4]}))
    ranked.sort(key=lambda row:(-row[0],row[1]))
    return [row[2] for row in ranked[:max(1,min(limit,8))]]


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path.cwd())
    parser.add_argument('--query',required=True)
    parser.add_argument('--limit',type=int,default=3)
    parser.add_argument('--index',type=Path)
    parser.add_argument('--refresh',action='store_true')
    parser.add_argument('--no-cache',action='store_true')
    args=parser.parse_args();root=args.root.resolve()
    key=hashlib.sha256(str(root).encode()).hexdigest()[:20]
    index=args.index or Path(tempfile.gettempdir())/'diazverso-context'/f'{key}.json'
    if not args.no_cache and index.resolve().is_relative_to(root):
        parser.error('Store the disposable index outside plugin source')
    previous={}
    if not args.no_cache and index.is_file() and not index.is_symlink():
        try:previous=json.loads(index.read_text('utf-8'))
        except (ValueError,OSError):pass
    if args.index and not args.no_cache and index.exists() and (index.is_symlink() or not isinstance(previous,dict)
            or previous.get('schema_version')!=VERSION or previous.get('root_key')!=key):
        parser.error('Custom index already exists and is not this plugin context cache')
    graph=build(root,{} if args.refresh else previous)
    cache_status='DISABLED' if args.no_cache else 'AVAILABLE'
    if not args.no_cache:
        try:
            index.parent.mkdir(parents=True,exist_ok=True)
            fd,tmp=tempfile.mkstemp(prefix='.graph-',dir=index.parent)
            try:
                with os.fdopen(fd,'w',encoding='utf-8') as writer:json.dump(graph,writer,ensure_ascii=False)
                os.replace(tmp,index)
            finally:
                if Path(tmp).exists():Path(tmp).unlink()
        except OSError:cache_status='UNAVAILABLE'
    print(json.dumps({'stats':graph['stats'],'cache':cache_status,'matches':find(graph,args.query,args.limit)},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
