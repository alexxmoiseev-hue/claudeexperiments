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
python -m hunter discover "B2B SaaS companies in Germany with 50-200 employees"
python -m hunter leads "B2B SaaS companies in Germany" --companies 5 --per-company 3 \
    --seniority executive,senior > leads.csv
```

`discover` is free. `leads` runs Discover, then a Domain Search per company (1 credit per 10
emails returned, so at most `--companies` credits with `--per-company` ≤ 10), and prints a CSV
with the same columns as OpenOutreach's export (`email, first_name, last_name, company, title,
website, linkedin_url, reason, lead_id, qualified_at`), ready to import into Instantly,
Smartlead or HubSpot. `reason` is left blank for the qualification step.

The key is sent in the `X-API-KEY` header, never in the URL.

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
