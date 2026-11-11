"""D07/L06: synthetic offline packages only; no Drive or Remotion use."""
import hashlib
import importlib.util
import json
import struct
import tempfile
import unittest
import zipfile
import zlib
from pathlib import Path

SOURCE=Path(__file__).resolve().parents[1]/"scripts"/"verify_offline_package.py"
spec=importlib.util.spec_from_file_location("diazverso_offline_package",SOURCE)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def chunk(tag,body):
    return struct.pack(">I",len(body))+tag+body+struct.pack(">I",zlib.crc32(tag+body))


def png():
    hdr=struct.pack(">IIBBBBB",4,4,8,6,0,0,0)
    scan=(b"\x00"+bytes([20,40,60,255])*4)*4
    return mod.PNG_SIG+chunk(b"IHDR",hdr)+chunk(b"IDAT",zlib.compress(scan))+chunk(b"IEND",b"")


def contents():
    image=png()
    blob=hashlib.sha1(b"blob "+str(len(image)).encode()+b"\0"+image).hexdigest()
    catalog={"assets":[{"id":"brand.nox.canonical","path":"assets/brand/nox/Nox.png",
                        "size_bytes":len(image),"git_blob_sha1":blob,
                        "dimensions":{"width":4,"height":4}}]}
    plugin={"name":"diazverso","extensions":{"com.openai":{
        "onboardingSkill":"./skills/diazverso-setup/SKILL.md"}}}
    files={p:b"local fixture" for p in mod.REQUIRED}
    files["plugin.json"]=json.dumps(plugin).encode()
    files["assets/manifest.json"]=json.dumps(catalog).encode()
    files["assets/brand/nox/Nox.png"]=image
    for external in mod.EXTERNAL:
        files[f"skills/{external}/SKILL.md"]=b"---\nname: test\n---"
        files[f"skills/{external}/LICENSE"]=b"fixture permission"
    return files


class OfflinePackageTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)/"diazverso-test.zip"

    def write(self, files):
        with zipfile.ZipFile(self.path,"w",compression=zipfile.ZIP_DEFLATED) as z:
            for name,data in files.items():
                z.writestr(name,data)

    def test_offline_valid_package(self):
        self.write(contents())
        out=mod.verify(self.path)
        self.assertEqual(out["status"],"OFFLINE_MEDIA_AND_PACKAGE_STRUCTURE_VALID")
        self.assertEqual(out["nox"]["width"],4)
        self.assertFalse(out["drive_accessed"])
        self.assertFalse(out["runtime_rendered"])
        self.assertFalse(out["host_installed"])
        self.assertFalse(out["nox_visually_reviewed"])
        self.assertFalse(out["publishing_performed"])

    def test_missing_nox_blocks(self):
        data=contents()
        del data["assets/brand/nox/Nox.png"]
        self.write(data)
        with self.assertRaises(ValueError): mod.verify(self.path)

    def test_modified_nox_rejected_by_hash(self):
        data=contents()
        data["assets/brand/nox/Nox.png"]=data["assets/brand/nox/Nox.png"]+b"modified"
        self.write(data)
        with self.assertRaises(ValueError): mod.verify(self.path)

    def test_missing_license_blocks(self):
        data=contents()
        del data["skills/context-optimization/LICENSE"]
        self.write(data)
        with self.assertRaises(ValueError): mod.verify(self.path)

    def test_path_traversal_rejected(self):
        data=contents()
        data["../danger"]=b"no"
        self.write(data)
        with self.assertRaises(ValueError): mod.verify(self.path)

    def test_duplicate_member_rejected(self):
        self.write(contents())
        with zipfile.ZipFile(self.path,"a") as z:
            z.writestr("plugin.json",b"duplicate")
        with self.assertRaises(ValueError): mod.verify(self.path)

    def test_wrong_onboarding_rejected(self):
        data=contents()
        config=json.loads(data["plugin.json"])
        config["extensions"]["com.openai"]["onboardingSkill"]="./skills/other/SKILL.md"
        data["plugin.json"]=json.dumps(config).encode()
        self.write(data)
        with self.assertRaises(ValueError): mod.verify(self.path)

    def test_nonzip_rejected(self):
        self.path.write_bytes(b"not a zip")
        with self.assertRaises(zipfile.BadZipFile): mod.verify(self.path)

    def test_no_nox_manifest_entry_rejected(self):
        data=contents()
        data["assets/manifest.json"]=json.dumps({"assets":[]}).encode()
        self.write(data)
        with self.assertRaises(ValueError): mod.verify(self.path)

    def test_missing_setup_rejected(self):
        data=contents()
        del data["skills/diazverso-setup/SKILL.md"]
        self.write(data)
        with self.assertRaises(ValueError): mod.verify(self.path)


if __name__=="__main__":unittest.main()
