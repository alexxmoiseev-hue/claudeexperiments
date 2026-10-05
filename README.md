# Hunter.io API client

Lightweight Python client and CLI for the [Hunter.io API v2](https://hunter.io/api-documentation/v2). No third-party dependencies.

## Setup

```bash
cp .env.example .env   # then put your key into HUNTER_API_KEY
```

The key is read from the `HUNTER_API_KEY` environment variable or from `.env` (which is git-ignored).

## CLI

```bash
python -m hunter account
python -m hunter domain-search stripe.com --limit 5
python -m hunter email-finder stripe.com Patrick Collison
python -m hunter verify patrick@stripe.com
python -m hunter count stripe.com
```

## Python

```python
from hunter import HunterClient

client = HunterClient()
result = client.domain_search("stripe.com", limit=5)
for e in result["emails"]:
    print(e["value"], e.get("position"))
```

## Tests

```bash
python -m unittest discover tests
```
