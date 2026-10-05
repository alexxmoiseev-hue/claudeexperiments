import json
import os
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://api.hunter.io/v2"


class HunterError(Exception):
    def __init__(self, status, errors):
        self.status = status
        self.errors = errors
        details = "; ".join(e.get("details", str(e)) for e in errors) or "unknown error"
        super().__init__(f"Hunter API error {status}: {details}")


def _load_dotenv(path=".env"):
    """Load KEY=VALUE pairs from a .env file without overriding existing env vars."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("'\""))


class HunterClient:
    def __init__(self, api_key=None, timeout=30):
        if api_key is None:
            _load_dotenv()
            api_key = os.environ.get("HUNTER_API_KEY")
        if not api_key:
            raise ValueError("Hunter API key not set: pass api_key or set HUNTER_API_KEY")
        self.api_key = api_key
        self.timeout = timeout

    def _get(self, path, **params):
        params = {k: v for k, v in params.items() if v is not None}
        params["api_key"] = self.api_key
        url = f"{BASE_URL}/{path}?{urllib.parse.urlencode(params)}"
        try:
            with urllib.request.urlopen(url, timeout=self.timeout) as resp:
                return json.load(resp)["data"]
        except urllib.error.HTTPError as e:
            try:
                errors = json.load(e).get("errors", [])
            except ValueError:
                errors = []
            raise HunterError(e.code, errors) from None

    def domain_search(self, domain=None, company=None, limit=10, offset=0,
                      type=None, seniority=None, department=None):
        """Find email addresses for a domain or company name."""
        return self._get("domain-search", domain=domain, company=company, limit=limit,
                         offset=offset, type=type, seniority=seniority, department=department)

    def email_finder(self, first_name, last_name, domain=None, company=None):
        """Find the most likely email address of a person."""
        return self._get("email-finder", first_name=first_name, last_name=last_name,
                         domain=domain, company=company)

    def email_verifier(self, email):
        """Verify the deliverability of an email address."""
        return self._get("email-verifier", email=email)

    def email_count(self, domain=None, company=None, type=None):
        """Count email addresses Hunter has for a domain (free, no credits used)."""
        return self._get("email-count", domain=domain, company=company, type=type)

    def account(self):
        """Return account information and remaining request quota."""
        return self._get("account")
