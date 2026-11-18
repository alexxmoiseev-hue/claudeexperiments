import csv
import io
import unittest
from unittest import mock

from hunter.leads import COLUMNS, find_leads, write_csv


class FindLeadsTest(unittest.TestCase):
    def setUp(self):
        self.client = mock.Mock()
        self.client.discover.return_value = [
            {"domain": "acme.io", "organization": "Acme"},
            {"organization": "No Domain Inc"},
            {"domain": "beta.dev", "organization": "Beta"},
        ]
        self.client.domain_search.side_effect = lambda domain, **kw: {
            "acme.io": {"organization": "Acme Corp", "emails": [
                {"value": "jane@acme.io", "first_name": "Jane", "last_name": "Doe",
                 "position": "VP Sales", "linkedin": "https://linkedin.com/in/jane"},
            ]},
            "beta.dev": {"organization": None, "emails": [
                {"value": "bob@beta.dev", "first_name": None, "last_name": None},
            ]},
        }[domain]

    def test_rows_from_discover_and_domain_search(self):
        rows = list(find_leads(self.client, "B2B SaaS", companies=3, per_company=2,
                               seniority="executive", log=io.StringIO()))
        self.client.discover.assert_called_once_with(query="B2B SaaS", limit=3)
        self.client.domain_search.assert_any_call("acme.io", limit=2, type="personal",
                                                  seniority="executive", department=None)
        self.assertEqual([r["email"] for r in rows], ["jane@acme.io", "bob@beta.dev"])
        self.assertEqual(rows[0]["company"], "Acme Corp")
        self.assertEqual(rows[0]["title"], "VP Sales")
        self.assertEqual(rows[0]["lead_id"], "jane@acme.io")
        # Falls back to Discover's name and blanks out missing fields.
        self.assertEqual(rows[1]["company"], "Beta")
        self.assertEqual(rows[1]["first_name"], "")

    def test_companies_caps_domain_searches(self):
        list(find_leads(self.client, "x", companies=1, log=io.StringIO()))
        self.assertEqual(self.client.domain_search.call_count, 1)

    def test_write_csv_uses_openoutreach_columns(self):
        out = io.StringIO()
        count = write_csv(find_leads(self.client, "x", log=io.StringIO()), out)
        self.assertEqual(count, 2)
        reader = csv.DictReader(io.StringIO(out.getvalue()))
        self.assertEqual(reader.fieldnames, COLUMNS)
        self.assertEqual(next(reader)["linkedin_url"], "https://linkedin.com/in/jane")


if __name__ == "__main__":
    unittest.main()
