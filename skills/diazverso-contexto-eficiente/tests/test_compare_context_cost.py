import importlib.util
import unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts"/"compare_context_cost.py"
s=importlib.util.spec_from_file_location("diazverso_cost",P)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def pairs():
    return [{"task_id":f"T{i}","baseline":{"input_tokens":1000,"output_tokens":400,"tool_calls":10,"success":True,"source":"measured-baseline"},
             "optimized":{"input_tokens":600,"output_tokens":300,"tool_calls":7,"success":True,"source":"measured-after"}}
            for i in range(3)]
class CostTests(unittest.TestCase):
    def test_three_pairs_have_arithmetic_not_claimed_measurements(self):
        r=m.compare(pairs())
        self.assertEqual(r["total_token_change_percent"],-35.71)
        self.assertFalse(r["host_measurements_authenticated_by_code"])
    def test_requires_three_pairs(self):
        with self.assertRaises(ValueError):m.compare(pairs()[:2])
    def test_duplicate_tasks_rejected(self):
        p=pairs();p[1]["task_id"]=p[0]["task_id"]
        with self.assertRaises(ValueError):m.compare(p)
    def test_quality_regression_prevents_success(self):
        p=pairs();p[1]["optimized"]["success"]=False
        self.assertEqual(m.compare(p)["status"],"QUALITY_REGRESSION_OR_INVALID_RESULT")
    def test_estimates_are_not_accepted_as_fields(self):
        p=pairs();p[0]["optimized"]["estimated_tokens"]=50
        with self.assertRaises(ValueError):m.compare(p)
    def test_string_token_metric_rejected(self):
        p=pairs();p[0]["optimized"]["input_tokens"]="600"
        with self.assertRaises(ValueError):m.compare(p)
if __name__=="__main__":unittest.main()
