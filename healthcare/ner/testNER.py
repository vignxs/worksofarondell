import json
import collections

json_string = """
{
    "a": 1,
  
    "c": {"x":1, "y":2, "z":3, "a":4}
}
"""

def detect_duplicate_keys(list_of_pairs):
    key_count = collections.Counter(k for k,v in list_of_pairs)
    duplicate_keys = ', '.join(k for k,v in key_count.items() if v>1)

    if len(duplicate_keys) != 0:
        raise ValueError('Duplicate key(s) found: {}'.format(duplicate_keys))

def validate_data(list_of_pairs):
    detect_duplicate_keys(list_of_pairs)
    # More dectection, each of them will raise exception upon invalid
    # data
    return dict(list_of_pairs)


obj = json.loads(json_string, object_pairs_hook=validate_data)
print(obj)