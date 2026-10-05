import io
import json
import unittest
import urllib.error
from unittest import mock

from hunter import HunterClient, HunterError


def _response(payload):
    return io.BytesIO(json.dumps(payload).encode())


class HunterClientTest(unittest.TestCase):
    def setUp(self):
        self.client = HunterClient(api_key="test-key")

    @mock.patch("urllib.request.urlopen")
    def test_domain_search_builds_url_and_returns_data(self, urlopen):
        urlopen.return_value = _response({"data": {"domain": "stripe.com", "emails": []}})
        data = self.client.domain_search("stripe.com", limit=5)
        self.assertEqual(data["domain"], "stripe.com")
        url = urlopen.call_args[0][0]
        self.assertIn("/domain-search?", url)
        self.assertIn("domain=stripe.com", url)
        self.assertIn("limit=5", url)
        self.assertIn("api_key=test-key", url)
        self.assertNotIn("company=", url)

    @mock.patch("urllib.request.urlopen")
    def test_http_error_raises_hunter_error(self, urlopen):
        body = _response({"errors": [{"id": "wrong_params", "details": "bad domain"}]})
        urlopen.side_effect = urllib.error.HTTPError("u", 400, "Bad", {}, body)
        with self.assertRaises(HunterError) as ctx:
            self.client.email_verifier("x")
        self.assertEqual(ctx.exception.status, 400)
        self.assertIn("bad domain", str(ctx.exception))

    def test_missing_key_raises(self):
        with mock.patch.dict("os.environ", {}, clear=True), \
             mock.patch("hunter.client._load_dotenv"):
            with self.assertRaises(ValueError):
                HunterClient()


if __name__ == "__main__":
    unittest.main()
