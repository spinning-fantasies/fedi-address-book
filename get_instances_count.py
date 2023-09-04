import json
from collections import defaultdict

def count_all_instances(json_file):
    # Load the JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Create a defaultdict to store the counts of instances
    instance_counts = defaultdict(int)

    # Iterate through the data and count instances
    for item in data:
        # Assuming the 'acct' field contains the instance address
        acct = item.get('acct')
        if acct:
            # Extract the instance address by splitting on '@'
            instance = acct.split('@')[-1]
            instance_counts[instance] += 1

    return instance_counts

# Example usage:
json_file_path = 'followers.json'
instance_counts = count_all_instances(json_file_path)

# Print the counts for all instances
for instance, count in instance_counts.items():
    print(f"Instance: {instance}, Count: {count}")
