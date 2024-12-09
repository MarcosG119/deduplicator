import json
import argparse

def load_json(file_path):
    '''
    Load JSON file from the given path
    args:
        file_path: str: path to JSON file
    return: 
        dict: JSON data
    '''
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None
    


def log_changes(original, updated):
    '''
    Log changes between two dictionaries
    args:
        original: dictionary before being updated
        updated: dictionary after being updated
    return:
        list: list of changes
    '''
    changes = []
    for key in updated.keys():
        if original[key] != updated[key]:
            changes.append({
                "field": key,
                "from": original[key],
                "to": updated[key]
            })
    return changes


def deduplicate_by_key(key, data, log):
    '''
    Deduplicate an array of dictionaries by a given key
    args:
        key: str: key to deduplicate by
        data: list: array of dictionaries
        log: list: log of changes
    return:
        list: deduplicated array of dictionaries
    '''
    deduplicated = {} # store deduplicated records
    for index, record in enumerate(data): # use enumerate to keep track of index
        value = record[key]
        if value not in deduplicated:
            deduplicated[value] = (record, index)
        else:
            current_record, current_index = deduplicated[value]
            # compare entryDates and indices to keep the most recent record
            if (record['entryDate'] > current_record['entryDate'] 
                or (record['entryDate'] == current_record['entryDate'] 
                    and index > current_index)):
                deduplicated[value] = (record, index)
                # log changes
                log.append({
                    "source": current_record,
                    "updated": record,
                    "changes": log_changes(current_record, record)
                })
    return [item[0] for item in deduplicated.values()]


def deduplicate(data, keys=['email', '_id']):
    '''
    Deduplicate JSON records
    
    I chose to deduplicate by 1 key at a time to keep the code simple and easy to understand. Another approach would be to deduplicate by email and _id at the same time, but that would require more complex array logic and nested loops to be able to do comparisons and matching the objects correctly by both ids.
    
    This approach is more understandable and easier to debug. If the data set is very large, this approach may not be the best one. It also allows for deduplicating by any key we desire, as the keys are passed as arguments.
    
    args:
        data: list: array of dictionaries
        keys: list: keys to deduplicate by
    return:
        list: deduplicated array of dictionaries
        list: log of changes
    '''
    changeLog = []
    for key in keys:
        data = deduplicate_by_key(key, data, changeLog)
    return data, changeLog


def main():
    parser = argparse.ArgumentParser(description="Deduplicate JSON records.")
    parser.add_argument("input_file", help="Path to input JSON file")
    parser.add_argument("output_file", help="Path to output JSON file")
    parser.add_argument("--log", help="Path to log file", default="deduplication_log.json")
    args = parser.parse_args()

    data = load_json(args.input_file)
    leads = data['leads']

    deduplicated_data, change_log = deduplicate(leads)

    with open(args.output_file, 'w') as output:
        json.dump({"leads": deduplicated_data}, output, indent=4)

    with open(args.log, 'w') as log_file:
        json.dump(change_log, log_file, indent=4)

    print(f"Deduplicated data saved to {args.output_file}")
    print(f"Log saved to {args.log}")


if __name__ == '__main__':
    main()
