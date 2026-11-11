#!/usr/bin/env python3
"""context-metrics — compare actual telemetry for three identical tasks, no model calls.

All values must come from measured host/API usage. Character counts and
estimated token counts are not accepted. Quality must not regress.
"""
from __future__ import annotations
import argparse
import json
import statistics
from pathlib import Path

def compare(records: list[dict]) -> dict:
    if not isinstance(records,list) or len(records)<3:
        raise ValueError("At least three matched task pairs are required")
    ids=set();pairs=[]
    for r in records:
        if not isinstance(r,dict) or set(r)!={"task_id","baseline","optimized"}:
            raise ValueError("Missing pair fields")
        tid=r["task_id"]
        if not isinstance(tid,str) or not tid.strip() or tid in ids:
            raise ValueError("Invalid/duplicated task id")
        ids.add(tid)
        for label in ("baseline","optimized"):
            run=r[label]
            if not isinstance(run,dict) or set(run)!={"input_tokens","output_tokens",
                                                       "tool_calls","success","source"}:
                raise ValueError("Run requires measured telemetry and success")
            for key in ("input_tokens","output_tokens","tool_calls"):
                if type(run[key]) is not int or run[key]<0:
                    raise ValueError("Telemetry must be actual nonnegative integers")
            if type(run["success"]) is not bool or not isinstance(run["source"],str) or not run["source"].strip():
                raise ValueError("Source receipt and verified correctness required")
        a=r["baseline"];b=r["optimized"]
        a_tokens=a["input_tokens"]+a["output_tokens"]
        b_tokens=b["input_tokens"]+b["output_tokens"]
        if not a_tokens:
            raise ValueError("Baseline token count cannot be zero")
        pairs.append({"task_id":tid,"before_tokens":a_tokens,
                      "after_tokens":b_tokens,
                      "token_change_percent":round((b_tokens/a_tokens-1)*100,2),
                      "before_tool_calls":a["tool_calls"],
                      "after_tool_calls":b["tool_calls"],
                      "quality_preserved":a["success"] and b["success"]})
    all_good=all(p["quality_preserved"] for p in pairs)
    return {"status":"MEASURED_AND_QUALITY_PRESERVED" if all_good else "QUALITY_REGRESSION_OR_INVALID_RESULT",
            "pairs":pairs,"total_token_change_percent":round(
                (sum(p["after_tokens"] for p in pairs)/
                 sum(p["before_tokens"] for p in pairs)-1)*100,2),
            "median_token_change_percent":round(statistics.median(
                p["token_change_percent"] for p in pairs),2),
            "all_successful":all_good,
            "host_measurements_authenticated_by_code":False,
            "external_calls_performed":False,"publishing_performed":False}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("telemetry_json",type=Path)
    a=p.parse_args()
    print(json.dumps(compare(json.loads(a.telemetry_json.read_text("utf-8"))),
                     ensure_ascii=False,indent=2))
if __name__=="__main__":main()
