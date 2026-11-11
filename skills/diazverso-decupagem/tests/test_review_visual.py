"""J03: real synthetic PNG bytes with CRC, compression and J02 hash receipts."""
import hashlib
import importlib.util
import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("diazverso_review_visual",ROOT/"scripts"/"review_visual.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def chunk(tag, payload):
    return struct.pack(">I",len(payload))+tag+payload+struct.pack(">I",zlib.crc32(tag+payload))


def png(width=32,height=32,pixel=None,channels=3):
    if pixel is None:
        pixel=lambda x,y:(30+x*5,30+y*5,70)
    raw=bytearray()
    for y in range(height):
        raw.append(0)
        line=bytearray()
        for x in range(width):
            line.extend(pixel(x,y))
        raw.extend(line)
    color=6 if channels==4 else 2
    ihdr=struct.pack(">IIBBBBB",width,height,8,color,0,0,0)
    return mod.PNG_SIGNATURE+chunk(b"IHDR",ihdr)+chunk(b"IDAT",zlib.compress(bytes(raw)))+chunk(b"IEND",b"")


class VisualReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder=Path(self.temp.name)

    def receipt(self,frame,content,reason="S01:entry"):
        path=self.folder/f"frame_{frame:06d}.png"
        path.write_bytes(content)
        return {"frame":frame,"path":str(path),"sha256":hashlib.sha256(content).hexdigest(),"reasons":[reason]}

    def test_valid_gradient_frame(self):
        row=self.receipt(0,png())
        r=mod.review({"frames":[row]},fps=30)
        self.assertEqual(r["frames_analyzed"],1)
        self.assertFalse(r["visual_qa_approved_by_code"])
        self.assertFalse(r["nox_identity_recognized"])
        self.assertIn("nox_identidade",r["manual_pending"])

    def test_uniform_frame_review_flag(self):
        row=self.receipt(0,png(pixel=lambda x,y:(50,50,50)))
        codes=[x["code"] for x in mod.review({"frames":[row]},fps=30)["findings"]]
        self.assertIn("LOW_TONAL_VARIATION",codes)

    def test_dark_edges_review_flag(self):
        image=png(pixel=lambda x,y:(0,0,0) if x in (0,31) or y in (0,31) else (180,180,180))
        r=mod.review({"frames":[self.receipt(0,image)]},fps=30)
        self.assertIn("DARK_FRAME_BORDER",[x["code"] for x in r["findings"]])

    def test_identical_distant_frames_flagged(self):
        image=png()
        rows=[self.receipt(0,image),self.receipt(45,image,"S01:middle")]
        r=mod.review({"frames":rows},fps=30)
        self.assertIn("NEAR_IDENTICAL_SAMPLED_FRAMES",[x["code"] for x in r["findings"]])

    def test_adjacent_black_white_flash_flagged(self):
        a=png(pixel=lambda x,y:(0,0,0))
        b=png(pixel=lambda x,y:(255,255,255))
        rows=[self.receipt(89,a),self.receipt(90,b)]
        r=mod.review({"frames":rows},fps=30)
        self.assertIn("ABRUPT_VISUAL_CHANGE",[x["code"] for x in r["findings"]])

    def test_original_sha_must_match(self):
        row=self.receipt(0,png())
        row["sha256"]="0"*64
        with self.assertRaises(ValueError):
            mod.review({"frames":[row]},fps=30)

    def test_corrupt_png_crc_rejected(self):
        data=bytearray(png())
        data[50]^=1
        row=self.receipt(0,bytes(data))
        with self.assertRaises(ValueError):
            mod.review({"frames":[row]},fps=30)

    def test_real_alpha_channel_flagged(self):
        image=png(pixel=lambda x,y:(255,30,30,0),channels=4)
        result=mod.review({"frames":[self.receipt(0,image)]},fps=30)
        self.assertIn("TRANSPARENCY_IN_OUTPUT",[x["code"] for x in result["findings"]])

    def test_wrong_filename_rejected(self):
        row=self.receipt(0,png())
        row["frame"]=1
        with self.assertRaises(ValueError):
            mod.review({"frames":[row]},fps=30)

    def test_out_of_order_manifest_rejected(self):
        rows=[self.receipt(30,png()),self.receipt(0,png())]
        with self.assertRaises(ValueError):
            mod.review({"frames":rows},fps=30)

    def test_manual_approval_requires_evidence(self):
        row=self.receipt(0,png())
        manual={k:{"status":"APROVADO","evidence":""} for k in mod.CHECKS}
        with self.assertRaises(ValueError):
            mod.review({"frames":[row]},fps=30,manual=manual)

    def test_human_notes_never_become_machine_verified(self):
        row=self.receipt(0,png())
        manual={k:{"status":"APROVADO","evidence":"Inspeção visual anotada"}
                for k in mod.CHECKS}
        result=mod.review({"frames":[row]},fps=30,manual=manual)
        self.assertEqual(result["manual_pending"],[])
        self.assertFalse(result["visual_qa_approved_by_code"])
        self.assertFalse(result["motion_continuity_verified"])

    def test_wrong_dimensions_rejected(self):
        rows=[self.receipt(0,png(width=32,height=32)),self.receipt(30,png(width=40,height=32))]
        with self.assertRaises(ValueError):
            mod.review({"frames":rows},fps=30)

    def test_too_many_manifest_entries_rejected(self):
        data={"frames":[self.receipt(0,png())]*121}
        with self.assertRaises(ValueError):
            mod.review(data,fps=30)

    def test_missing_extraction_is_not_accepted(self):
        with self.assertRaises(ValueError):
            mod.review({"status":"SAMPLING_PLAN","steps":[]},fps=30)


if __name__=="__main__":
    unittest.main()
