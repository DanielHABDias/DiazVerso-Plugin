"""resume: portable resume checkpoint with freshness, digest and duplicate guards.

Read-only decisions: persistence and connected source readback remain host duties.
Never makes remote writes, renders or publishes videos.
"""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path

PROD = re.compile(r'(?:TF|VD|SH)_\d{4,}\Z')
TASK = re.compile(r'[a-z][a-z0-9_-]{1,63}\Z')


def _validate(state: dict, *, latest: bool = False) -> None:
    required = {'production_id', 'revision', 'next_task', 'completed', 'source_ref'}
    if latest:
        required |= {'fresh_read'}
    if not isinstance(state, dict) or set(state) != required:
        raise ValueError('Invalid state keys')
    if not isinstance(state['production_id'], str) or not PROD.fullmatch(state['production_id']):
        raise ValueError('Invalid production ID')
    if type(state['revision']) is not int or state['revision'] < 0:
        raise ValueError('Invalid revision')
    if not isinstance(state['source_ref'], str) or not state['source_ref'].strip():
        raise ValueError('Source reference is required')
    if state['next_task'] is not None and (not isinstance(state['next_task'], str) or not TASK.fullmatch(state['next_task'])):
        raise ValueError('Invalid next task')
    tasks = state['completed']
    if not isinstance(tasks, list) or any(not isinstance(x, str) or not TASK.fullmatch(x) for x in tasks):
        raise ValueError('Invalid completed tasks')
    if len(set(tasks)) != len(tasks) or state['next_task'] in tasks:
        raise ValueError('Repeated or already completed next task')
    if latest and state['fresh_read'] is not True:
        raise ValueError('Current source must have verified fresh readback')


def checkpoint(source: dict) -> dict:
    _validate(source)
    payload = {k: source[k] for k in ('production_id', 'revision', 'next_task', 'completed', 'source_ref')}
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
    return {'schema': 'diazverso-resume-v1', 'source': payload,
            'sha256': hashlib.sha256(blob).hexdigest(),
            'write_performed': False, 'publication_performed': False}


def recover(saved: dict, latest: dict) -> dict:
    if not isinstance(saved, dict) or set(saved) != {'schema', 'source', 'sha256', 'write_performed', 'publication_performed'}:
        raise ValueError('Invalid checkpoint envelope')
    if saved['schema'] != 'diazverso-resume-v1' or saved['write_performed'] is not False or saved['publication_performed'] is not False:
        raise ValueError('Unsafe checkpoint')
    expected = checkpoint(saved['source'])['sha256']
    if saved['sha256'] != expected:
        raise ValueError('Checkpoint was modified')
    _validate(latest, latest=True)
    prior = saved['source']
    if latest['production_id'] != prior['production_id'] or latest['source_ref'] != prior['source_ref']:
        raise ValueError('Cannot continue from a different production/source')
    if latest['revision'] < prior['revision']:
        return {'status': 'BLOCKED_STALE_READBACK', 'next_task': None,
                'reason': 'Connected source revision is older than checkpoint', 'write_performed': False}
    if latest['completed'][:len(prior['completed'])] != prior['completed']:
        return {'status': 'BLOCKED_HISTORY_CONFLICT', 'next_task': None,
                'reason': 'Completed task history diverged', 'write_performed': False}
    if latest['revision'] == prior['revision'] and any(
        latest[key] != prior[key] for key in ('next_task', 'completed')
    ):
        return {'status': 'BLOCKED_REVISION_CONFLICT', 'next_task': None,
                'reason': 'Same revision has conflicting next task', 'write_performed': False}
    # Latest readback is authoritative. Never replay tasks present in completed.
    return {'status': 'RESUMABLE' if latest['next_task'] else 'NO_PENDING_TASK',
            'next_task': latest['next_task'], 'revision': latest['revision'],
            'completed_count': len(latest['completed']), 'write_performed': False,
            'publication_performed': False, 'fresh_readback_used': True}


def main() -> None:
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('checkpoint_json', type=Path)
    p.add_argument('latest_json', type=Path)
    a = p.parse_args()
    print(json.dumps(recover(json.loads(a.checkpoint_json.read_text('utf-8')),
                             json.loads(a.latest_json.read_text('utf-8'))), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
