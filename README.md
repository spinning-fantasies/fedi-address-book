# fedi-address-book
An address book for Fediverse followers

## Installation

Clone the repository :

```
git@github.com:spinning-fantasies/fedi-address-book.git
```

Activate a virtualenv :

```
cd fedi-address-book
python -m venv .
source ./bin/activate
```

Install the dependencies :

```
python -m pip install -r requirements.txt
```

Add environment variables to ``.env`` :

```
MASTODON_INSTANCE_URL=<your_mastodon_instance_url>
MASTODON_ACCESS_TOKEN=<your_mastodon_access_token>
AUTHENTICATED_USER_ID=<your_authenticated_user_id>
```

## Usage

Print the followers.json file

```
python print_json.py
```

Set up the database :

```
python setup_db.py
```

Launch the web server :

```
python main.py
```

Print the differences between two json files :

```
diff <(jq -S . file1.json) <(jq -S . file2.json)
```

