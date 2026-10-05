import argparse
import json
import sys

from .client import HunterClient, HunterError


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m hunter", description="Hunter.io API CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("account", help="show account info and quota")

    p = sub.add_parser("domain-search", help="find emails for a domain")
    p.add_argument("domain")
    p.add_argument("--limit", type=int, default=10)

    p = sub.add_parser("email-finder", help="find a person's email")
    p.add_argument("domain")
    p.add_argument("first_name")
    p.add_argument("last_name")

    p = sub.add_parser("verify", help="verify an email address")
    p.add_argument("email")

    p = sub.add_parser("count", help="count emails for a domain")
    p.add_argument("domain")

    args = parser.parse_args(argv)
    client = HunterClient()
    try:
        if args.command == "account":
            data = client.account()
        elif args.command == "domain-search":
            data = client.domain_search(args.domain, limit=args.limit)
        elif args.command == "email-finder":
            data = client.email_finder(args.first_name, args.last_name, domain=args.domain)
        elif args.command == "verify":
            data = client.email_verifier(args.email)
        else:
            data = client.email_count(args.domain)
    except HunterError as e:
        print(e, file=sys.stderr)
        return 1
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
