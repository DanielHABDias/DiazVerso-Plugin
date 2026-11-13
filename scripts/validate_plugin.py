#!/usr/bin/env python3
"""Validate the current plugin: manifests, skills, links, assets, SFX and Nox poses."""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXTERNAL=('find-broll',)
SKIP={'.git','node_modules','__pycache__','.cache','out','dist','build'}
SUFFIXES={'.md','.py','.json','.yaml','.yml','.ts','.tsx','.js','.mjs','.mts','.png','.jpg','.jpeg','.webp','.wav','.mp3','.svg','.txt','.ttf'}
HISTORY=re.compile(r'(?-i:\b[A-M]\d{2}\b)|refer[eê]ncia hist[oó]rica|^#{1,6}\s+.*(?:changelog|histórico de altera)|(?:20\d\d-\d{2}-\d{2}).*(?:altera|atualiza)',re.I|re.M)


def require(ok:bool,message:str)->None:
    if not ok:raise ValueError(message)


def resource_files(root:Path=ROOT)->list[Path]:
    files=[root/'plugin.json',root/'THIRD_PARTY_NOTICES.md',root/'.claude-plugin/plugin.json',root/'.claude-plugin/marketplace.json']
    for name in ('skills','assets','schemas','templates','hooks'):
        files.extend(p for p in (root/name).rglob('*') if p.is_file()
                     and not any(part in SKIP for part in p.relative_to(root).parts))
    return sorted(set(files))


def validate()->dict:
    manifest=json.loads((ROOT/'plugin.json').read_text())
    require(manifest.get('$schema')=='https://agent-plugins.org/schemas/1.0.0/plugin.schema.json','Invalid portable schema')
    require(manifest.get('name')=='diazverso','Plugin identity mismatch')
    require(bool(re.fullmatch(r'\d+\.\d+\.\d+',manifest.get('version',''))),'Invalid version')
    require(not any(k in manifest for k in ('skills','mcpServers','apps','interface')),'Non-portable manifest key')
    settings=manifest['extensions']['com.openai']
    require(settings['onboardingSkill']=='./skills/diazverso-contentlab/SKILL.md','Invalid onboarding')
    require(len(settings['interface']['shortDescription'])<=30,'Listing subtitle too long')
    market=json.loads((ROOT/'.agents/plugins/marketplace.json').read_text())
    require(market['name']=='diazverso' and len(market['plugins'])==1,'Invalid marketplace')
    entry=market['plugins'][0]
    require(entry['name']==manifest['name'] and entry['source']=={'source':'local','path':'./'},'Marketplace source mismatch')
    require(entry['category']==settings['interface']['category']=='Productivity','Marketplace category mismatch')
    require(entry['policy']=={'installation':'AVAILABLE','authentication':'ON_INSTALL'},'Invalid marketplace policy')
    claude=json.loads((ROOT/'.claude-plugin/plugin.json').read_text())
    require(claude['name']==manifest['name'] and claude['version']==manifest['version'],'Claude manifest out of sync with plugin.json')
    cmarket=json.loads((ROOT/'.claude-plugin/marketplace.json').read_text())
    require(cmarket['name']=='diazverso' and [e['name'] for e in cmarket['plugins']]==['diazverso'] and cmarket['plugins'][0]['source']=='./','Invalid Claude marketplace')
    hook=json.loads((ROOT/'hooks/hooks.json').read_text())['hooks']['SessionStart'][0]['hooks'][0]['command']
    require('skills/diazverso/SKILL.md' in hook and (ROOT/'skills/diazverso/SKILL.md').is_file(),'SessionStart hook must inject the entry skill')
    files=resource_files()+[ROOT/'README.md',ROOT/'AGENTS.md'];skill_count=0;python_count=0;js_count=0
    for file in files:
        rel=file.relative_to(ROOT).as_posix()
        require(not file.is_symlink() and file.resolve().is_relative_to(ROOT),'Unsafe path: '+rel)
        require(file.name=='LICENSE' or file.suffix in SUFFIXES,'Unexpected file: '+rel)
        require(file.name not in {'credentials.json','secret.json'} and not file.name.startswith('.env'),'Secret file: '+rel)
        if file.suffix in {'.md','.py','.ts','.tsx','.mjs','.mts','.json','.yaml','.yml'}:
            source=file.read_text('utf-8')
            if file.suffix=='.json':json.loads(source)
            if file.suffix=='.py':ast.parse(source,filename=rel);python_count+=1
            if file.suffix in {'.mjs','.js'} and shutil.which('node'):
                run=subprocess.run(['node','--check',str(file)],capture_output=True,text=True,timeout=15)
                require(run.returncode==0,'Invalid JS: '+rel+' '+run.stderr[-300:]);js_count+=1
            if file.name=='SKILL.md':
                fm=re.match(r'\A---\n(.*?)\n---\n',source,re.S)
                require(fm is not None,'Missing frontmatter: '+rel)
                require(re.search(r'^name:\s*'+re.escape(file.parent.name)+r'\s*$',fm[1],re.M) is not None,'Skill name mismatch: '+rel)
                require(re.search(r'^description:\s*\S.+$',fm[1],re.M) is not None,'Missing skill description: '+rel)
                desc=re.search(r'^description:\s*"?(.*?)"?\s*$',fm[1],re.M)[1]
                require(len(desc.split())<=60,'Skill description over 60 words (loaded every session): '+rel)
                skill_count+=1
            if file.suffix=='.md':
                require(not HISTORY.search(source),'Construction history in '+rel)
                for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)',source):
                    if re.match(r'^[a-z]+:',target) or target.startswith('#'):continue
                    dest=(file.parent/target.split('#')[0]).resolve()
                    require(dest.is_relative_to(ROOT) and dest.exists(),'Broken link: '+rel+' -> '+target)
                # Code-span resource links, excluding CLI syntax and data placeholders.
                for target in re.findall(r'`([^`\n]+)`',source):
                    if not re.fullmatch(r'(?:\.\./|\./)?[\w./-]+\.(?:md|py|json|tsx|ts|mjs|mts|yaml|yml|png)',target):continue
                    if '<' in target or '####' in target:continue
                    if '/' not in target and target not in {'plugin.json','README.md','THIRD_PARTY_NOTICES.md'}:continue
                    if target.startswith(('skills/','assets/','schemas/','templates/','scripts/')):
                        candidates=(ROOT/target,file.parent/target)
                    else:candidates=(file.parent/target,ROOT/target)
                    require(any(p.resolve().is_relative_to(ROOT) and p.exists() for p in candidates),'Broken resource: '+rel+' -> '+target)
            if file.suffix in {'.tsx','.ts','.mjs','.mts'}:
                for target in re.findall(r'(?:from\s*|import\s*)[\'\"](\.[^\'\"]+)[\'\"]',source):
                    base=file.parent/target
                    require(any(p.exists() for p in [base]+[Path(str(base)+s) for s in ('.ts','.tsx','.mjs','.mts','.js')]),'Broken import: '+rel+' -> '+target)
    for name in EXTERNAL:require((ROOT/f'skills/{name}/LICENSE').is_file(),'Missing license: '+name)
    catalog=json.loads((ROOT/'assets/manifest.json').read_text())
    for item in catalog['assets']:
        p=ROOT/item['path'];require(p.is_file() and p.resolve().is_relative_to(ROOT),'Missing asset')
        data=p.read_bytes();digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(len(data)==item['size_bytes'] and digest==item['git_blob_sha1'],'Asset integrity: '+item['path'])
    # O kit de motion é do Content Lab: o plugin não guarda cópia dele.
    require(not (ROOT/'skills/diazverso-motion/kit').exists(),'The motion kit belongs to the Content Lab; do not copy it into the plugin')
    # SFX de referência: cada WAV de assets/sfx/motion tem nome válido e está no guia de som.
    som=(ROOT/'skills/diazverso-motion/references/som.md').read_text()
    wavs={f.stem for f in (ROOT/'assets/sfx/motion').glob('*.wav')}
    missing=sorted(n for n in wavs if not re.fullmatch(r'[a-z0-9-]+',n) or f'`{n}`' not in som)
    require(not missing,'SFX without a valid name or missing from som.md: '+', '.join(missing))
    poses_dir=ROOT/'assets/brand/nox/poses'
    if poses_dir.is_dir():
        listed={item['path'] for item in catalog['assets']}
        pngs=sorted(f.name for f in poses_dir.glob('*.png'))
        for name in pngs:
            require(re.fullmatch(r'[a-z0-9-]+\.png',name) and f'assets/brand/nox/poses/{name}' in listed,'Pose PNG not named or not in assets/manifest.json: '+name)
            head=(poses_dir/name).read_bytes()[:24]
            require(head[:8]==b'\x89PNG\r\n\x1a\n' and 600<=int.from_bytes(head[20:24],'big')<=2400,'Pose PNG must be a PNG 600-2400 px tall: '+name)
        require(not (poses_dir/'poses.json').exists(),'poses.json is no longer supported; poses are ready-made PNGs in catalogo.json')
        # Catálogo: toda pose PNG pertence a exatamente uma pose do catálogo, com tons conhecidos.
        if pngs:
            cat_path=poses_dir/'catalogo.json'
            require(cat_path.is_file(),'Pose PNGs without assets/brand/nox/poses/catalogo.json')
            cat=json.loads(cat_path.read_text());tones=set(cat.get('tons',{}))
            owned=[]
            for key,entry in cat.get('poses',{}).items():
                files=entry.get('arquivos') or []
                require(re.fullmatch(r'[a-z0-9-]+',key) and files and all((poses_dir/f).is_file() for f in files),'Catalog pose without PNG: '+key)
                require(entry.get('gesto') and entry.get('olhos') and entry.get('tons') and set(entry['tons'])<=tones,'Catalog pose incomplete or unknown tone: '+key)
                owned+=files
            for name in pngs:
                require(owned.count(name)==1,'Pose PNG missing from catalogo.json (or listed twice): '+name)
    return {'status':'VALID','version':manifest['version'],'skills':skill_count,'resources':len(resource_files()),
            'python_syntax':python_count,'javascript_syntax':js_count,'references':'VALID'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--refresh-map',action='store_true',help='sem efeito; mantido por compatibilidade');parser.parse_args()
    print(json.dumps(validate(),ensure_ascii=False,indent=2))
