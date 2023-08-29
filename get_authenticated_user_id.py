import os
from mastodon import Mastodon
from dotenv import load_dotenv

load_dotenv()

# Replace these with your actual values
instance_url = os.getenv("MASTODON_INSTANCE_URL")
access_token = os.getenv("MASTODON_ACCESS_TOKEN")

# Create an instance of the Mastodon class
mastodon = Mastodon(
    access_token=access_token,
    api_base_url=instance_url
)

def get_authenticated_account_id():
    account = mastodon.account_verify_credentials()
    return account['id']

authenticated_account_id = get_authenticated_account_id()
print("Authenticated Account ID:", authenticated_account_id)