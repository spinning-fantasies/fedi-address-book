import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# Replace these with your actual values
instance_url = os.getenv("MASTODON_INSTANCE_URL")
access_token = os.getenv("MASTODON_ACCESS_TOKEN")
account_id = os.getenv("AUTHENTICATED_USER_ID")

# Set up headers
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Initialize variables
followers = []
next_page = f'{instance_url}/api/v1/accounts/{account_id}/followers'

while next_page:
    response = requests.get(next_page, headers=headers)

    if response.status_code == 200:
        data = response.json()
        followers.extend(data)
        next_page = response.links.get('next', {}).get('url')
    else:
        print("Error:", response.status_code)
        break


data = []

for follower in followers:

    data.append({
        'created_at': follower['created_at'].format().split("T")[0],
        'display_name': follower['display_name'],
        'acct': follower['acct']
    })

# Specify the file name
    filename = "followers.json"

    # Write the data to a JSON file
    with open(filename, "w") as json_file:
        json.dump(data, json_file)
        
print(f"JSON file {filename} created successfully.")
