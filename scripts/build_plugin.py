#!/usr/bin/env python3
"""Build a reproducible portable plugin archive from verified operational resources."""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from validate_plugin import ROOT, resource_files, validate


def package(output:Path)->dict:
    checks=validate()
    output=output.expanduser().resolve()
    if output==ROOT or ROOT in output.parents:raise ValueError('Write the ZIP outside plugin source')
    if output.exists():raise FileExistsError('Refuse to overwrite an existing package')
    output.parent.mkdir(parents=True,exist_ok=True)
    files=resource_files()
    try:
        with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED) as archive:
            for file in files:
                name=file.relative_to(ROOT).as_posix()
                member=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0))
                member.compress_type=zipfile.ZIP_DEFLATED;member.external_attr=0o644<<16
                archive.writestr(member,file.read_bytes())
        with zipfile.ZipFile(output) as archive:
            if archive.testzip() is not None:raise ValueError('Invalid archive CRC')
            if len(archive.namelist())!=len(set(archive.namelist())):raise ValueError('Duplicate archive member')
            for file in files:
                if archive.read(file.relative_to(ROOT).as_posix())!=file.read_bytes():raise ValueError('Source changed during packaging')
    except BaseException:
        if output.exists():output.unlink()
        raise
    return {'status':'PACKAGE_VALIDATED','version':checks['version'],'files':len(files),
            'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'bytes':output.stat().st_size,
            'output':str(output),'installed':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    print(json.dumps(package(a.output),ensure_ascii=False,indent=2))
