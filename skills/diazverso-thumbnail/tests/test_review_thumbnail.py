import hashlib
import importlib.util
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("review_thumbnail",ROOT/"scripts"/"review_thumbnail.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def png(width=1280,height=720):
    def chunk(tag,data):
        return struct.pack(">I",len(data))+tag+data+struct.pack(">I",zlib.crc32(tag+data)&0xffffffff)
    ihdr=struct.pack(">IIBBBBB",width,height,8,2,0,0,0)
    scan=(b"\x00"+bytes([20,30,40])*width)*height
    return mod.PNG_SIG+chunk(b"IHDR",ihdr)+chunk(b"IDAT",zlib.compress(scan))+chunk(b"IEND",b"")

def checks(nox=False):
    return {k:{"status":("NAO_APLICAVEL" if k=="nox_character_lock" and not nox else "APROVADO"),
               "evidence":"Conferência manual anotada com referência do arquivo"}
            for k in mod.VISUAL_CHECKS}

class ThumbnailReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.record={"production_id":"VD_0042","brief_id":"brief-v1",
                     "variants":{}}
        for key in ("A","B"):
            image=png()
            filename=f"VD_0042_{key}.png"
            (self.root/filename).write_bytes(image)
            self.record["variants"][key]={"path":filename,
                "drive_link":"https://drive.google.com/file/d/sample-"+key+"/view",
                "sha256":hashlib.sha256(image).hexdigest(),
                "nox_used":False,"visual_checks":checks(),"reviewer":"Revisor identificado"}

    def inspect(self):
        return mod.review(self.record,self.root)

    def test_valid_local_files_still_need_drive_readback(self):
        r=self.inspect()
        self.assertEqual(r["status"],"READY_FOR_EXTERNAL_REVIEW_AND_READBACK")
        self.assertFalse(r["drive_files_read_back"])
        self.assertFalse(r["ocr_performed"])
        self.assertFalse(r["nox_identity_recognized_by_code"])
        self.assertFalse(r["publishing_performed"])

    def test_dimensions_real_png(self):
        d=mod.dimensions(self.root/"VD_0042_A.png")
        self.assertEqual(d,(1280,720,"PNG_HEADER"))

    def test_wrong_dimensions_blocked(self):
        b=png(width=1024,height=768)
        path=self.root/"VD_0042_A.png"
        path.write_bytes(b)
        self.record["variants"]["A"]["sha256"]=hashlib.sha256(b).hexdigest()
        self.assertIn("DIMENSIONS_NOT_16_9_1280",
                      [x["code"] for x in self.inspect()["findings"]])

    def test_sha_tamper_blocked(self):
        self.record["variants"]["A"]["sha256"]="0"*64
        self.assertIn("FILE_SHA256_MISMATCH",
                      [x["code"] for x in self.inspect()["findings"]])

    def test_missing_local_image_blocked(self):
        (self.root/"VD_0042_B.png").unlink()
        self.assertEqual(self.inspect()["status"],"BLOCKED")

    def test_drive_link_untrusted_host_blocked(self):
        self.record["variants"]["A"]["drive_link"]="https://drive.google.com.evil.example/file/d/test"
        self.assertIn("DRIVE_LINK_MISSING_OR_INVALID",
                      [x["code"] for x in self.inspect()["findings"]])

    def test_nox_requires_human_identity_evidence(self):
        v=self.record["variants"]["A"]
        v["nox_used"]=True
        self.assertIn("HUMAN_CHECK_PENDING_NOX_CHARACTER_LOCK",
                      [x["code"] for x in self.inspect()["findings"]])

    def test_nox_approved_with_review_notes_is_not_machine_recognition(self):
        v=self.record["variants"]["A"]
        v["nox_used"]=True
        v["visual_checks"]=checks(nox=True)
        self.assertFalse(self.inspect()["nox_identity_recognized_by_code"])

    def test_false_human_approval_without_evidence_rejected(self):
        self.record["variants"]["A"]["visual_checks"]["mobile_text_legibility"]["evidence"]=""
        with self.assertRaises(ValueError):
            self.inspect()

    def test_outside_root_blocked(self):
        self.record["variants"]["A"]["path"]="../../outside.png"
        with self.assertRaises(ValueError):
            self.inspect()

    def test_corrupt_png_crc_fails(self):
        path=self.root/"VD_0042_A.png"
        image=bytearray(path.read_bytes())
        image[29]^=1
        path.write_bytes(image)
        self.record["variants"]["A"]["sha256"]=hashlib.sha256(image).hexdigest()
        self.assertEqual(self.inspect()["status"],"BLOCKED")

    def test_two_variants_required(self):
        self.record["variants"].pop("B")
        with self.assertRaises(ValueError):
            self.inspect()

if __name__=="__main__":
    unittest.main()
