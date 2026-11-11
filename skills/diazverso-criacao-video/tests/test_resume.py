import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
import importlib.util

SCRIPT=Path(__file__).resolve().parents[1]/"scripts"/"resume.py"
spec=importlib.util.spec_from_file_location("diazverso_resume",SCRIPT)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def state():
    return {'production_id':'VD_0008','revision':3,'next_task':'J03',
            'completed':['F07','H01'],'source_ref':'Sheets:Producoes:VD_0008'}

def latest(s=None):
    return {**(s or state()),'fresh_read':True}

class ResumeTests(unittest.TestCase):
    def test_same_revision(self):
        out=mod.recover(mod.checkpoint(state()),latest())
        self.assertEqual(out['next_task'],'J03')
        self.assertTrue(out['fresh_readback_used'])
    def test_second_process_cli_resume(self):
        with tempfile.TemporaryDirectory() as folder:
            d=Path(folder);a=d/'checkpoint.json';b=d/'latest.json'
            a.write_text(json.dumps(mod.checkpoint(state())));b.write_text(json.dumps(latest()))
            done=subprocess.run([sys.executable,str(SCRIPT),str(a),str(b)],capture_output=True,text=True,check=True)
            self.assertEqual(json.loads(done.stdout)['next_task'],'J03')
    def test_advance_from_fresh_source_without_replaying(self):
        now=state();now['revision']=4;now['completed'].append('J03');now['next_task']='J04'
        self.assertEqual(mod.recover(mod.checkpoint(state()),latest(now))['next_task'],'J04')
    def test_last_task_already_done(self):
        now=state();now['revision']=4;now['completed'].append('J03');now['next_task']=None
        self.assertEqual(mod.recover(mod.checkpoint(state()),latest(now))['status'],'NO_PENDING_TASK')
    def test_stale_readback_blocks(self):
        now=state();now['revision']=2
        self.assertEqual(mod.recover(mod.checkpoint(state()),latest(now))['status'],'BLOCKED_STALE_READBACK')
    def test_history_diverged_blocks(self):
        now=state();now['revision']=4;now['completed']=['F07','H02']
        self.assertEqual(mod.recover(mod.checkpoint(state()),latest(now))['status'],'BLOCKED_HISTORY_CONFLICT')
    def test_conflicting_same_revision_blocks(self):
        now=state();now['next_task']='J04'
        self.assertEqual(mod.recover(mod.checkpoint(state()),latest(now))['status'],'BLOCKED_REVISION_CONFLICT')
    def test_missing_fresh_read_rejected(self):
        with self.assertRaises(ValueError):mod.recover(mod.checkpoint(state()),{**state(),'fresh_read':False})
    def test_checksum_tampering_rejected(self):
        cp=mod.checkpoint(state());cp['source']['next_task']='J04'
        with self.assertRaises(ValueError):mod.recover(cp,latest())
    def test_completed_next_task_rejected(self):
        now=state();now['completed'].append('J03')
        with self.assertRaises(ValueError):mod.checkpoint(now)
    def test_duplicate_completed_rejected(self):
        now=state();now['completed'].append('F07')
        with self.assertRaises(ValueError):mod.checkpoint(now)
    def test_foreign_source_rejected(self):
        now=state();now['source_ref']='Sheets:Other'
        with self.assertRaises(ValueError):mod.recover(mod.checkpoint(state()),latest(now))
    def test_no_remote_side_effect(self):
        out=mod.recover(mod.checkpoint(state()),latest())
        self.assertFalse(out['write_performed']);self.assertFalse(out['publication_performed'])

if __name__ == '__main__':unittest.main()
