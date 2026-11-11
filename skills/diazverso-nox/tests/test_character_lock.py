import hashlib
import importlib.util
import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("lock_nox",ROOT/"scripts"/"character_lock.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def png(rgb=(30,50,80)):
    def chunk(tag,data):
        return struct.pack(">I",len(data))+tag+data+struct.pack(">I",zlib.crc32(tag+data))
    head=struct.pack(">IIBBBBB",4,4,8,2,0,0,0)
    raw=(b"\x00"+bytes(rgb)*4)*4
    return mod.PNG+chunk(b"IHDR",head)+chunk(b"IDAT",zlib.compress(raw))+chunk(b"IEND",b"")

class CharacterLockTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        original=png()
        base=self.root/"assets"/"brand"/"nox"/"Nox.png"
        base.parent.mkdir(parents=True)
        base.write_bytes(original)
        derivative=self.root/"assets"/"brand"/"nox"/"nox-pose-test.png"
        derivative.write_bytes(png((40,60,90)))
        blob=hashlib.sha1(f"blob {len(original)}\0".encode()+original).hexdigest()
        manifest={"assets":[{"id":"brand.nox.canonical",
                             "path":"assets/brand/nox/Nox.png",
                             "size_bytes":len(original),
                             "dimensions":{"width":4,"height":4},
                             "git_blob_sha1":blob}]}
        (self.root/"assets"/"manifest.json").write_text(json.dumps(manifest))
        self.data={"pose_path":"assets/brand/nox/nox-pose-test.png",
                   "canonical_manifest":"assets/manifest.json",
                   "pose_rights_evidence":"Teste sintético de pose, não Nox real",
                   "pose_purpose":"Verificar a ferramenta Character Lock",
                   "reviewer":"Revisor teste",
                   "checks":{k:{"status":"APROVADO","evidence":"Teste sintético sem prova de identidade"}
                             for k in mod.CHECKS}}
    def test_manifest_and_reference_checked(self):
        result=mod.review(self.data,self.root)
        self.assertTrue(result["pose_file_verified"])
        self.assertFalse(result["identity_recognized_by_code"])
        self.assertFalse(result["human_visual_comparison_authenticated_by_code"])
        self.assertFalse(result["publishing_performed"])
    def test_reference_bytes_modified_blocks(self):
        (self.root/"assets/brand/nox/Nox.png").write_bytes(png((0,0,0)))
        with self.assertRaises(ValueError):mod.review(self.data,self.root)
    def test_missing_pose_blocks(self):
        (self.root/"assets/brand/nox/nox-pose-test.png").unlink()
        with self.assertRaises(ValueError):mod.review(self.data,self.root)
    def test_original_not_accepted_as_derived_pose(self):
        self.data["pose_path"]="assets/brand/nox/Nox.png"
        with self.assertRaises(ValueError):mod.review(self.data,self.root)
    def test_pending_identity_is_not_approved(self):
        self.data["checks"]["facial_features"]["status"]="PENDENTE"
        result=mod.review(self.data,self.root)
        self.assertEqual(result["status"],"CHARACTER_LOCK_NOT_APPROVED")
    def test_missing_human_evidence_rejected(self):
        self.data["checks"]["palette"]["evidence"]=""
        with self.assertRaises(ValueError):mod.review(self.data,self.root)
    def test_untrusted_manifest_path_rejected(self):
        self.data["canonical_manifest"]="../../other.json"
        with self.assertRaises(ValueError):mod.review(self.data,self.root)
    def test_missing_rights_rejected(self):
        self.data["pose_rights_evidence"]=""
        with self.assertRaises(ValueError):mod.review(self.data,self.root)
    def test_incomplete_lock_checks_rejected(self):
        self.data["checks"].pop("no_redesign")
        with self.assertRaises(ValueError):mod.review(self.data,self.root)
    def test_nonpng_derivative_rejected(self):
        (self.root/"assets/brand/nox/nox-pose-test.png").write_bytes(b"fake")
        with self.assertRaises(ValueError):mod.review(self.data,self.root)

if __name__=="__main__":
    unittest.main()
