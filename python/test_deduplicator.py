from deduplicator import load_json, log_changes, deduplicate_by_key, deduplicate

def test_deduplicator():
  test_json = load_json("../test_leads.json")
  test_leads = test_json['test_leads']
  test_results = test_json['test_results']
  
  for i in range(len(test_leads)):
    result, _ = deduplicate(test_leads[i])
    assert result == test_results[i], f"Test failed for test case {i+1}"