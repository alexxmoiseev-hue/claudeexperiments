"""Turn an ICP description into a lead list: Discover companies, then Domain Search people at each."""
import csv
import sys

# Same columns, in the same order, as OpenOutreach's export, so the file imports into
# Instantly, Smartlead, HubSpot etc. without column mapping. `reason` is left blank here:
# it is filled in when each lead is qualified against the ICP.
COLUMNS = ["email", "first_name", "last_name", "company", "title", "website",
           "linkedin_url", "reason", "lead_id", "qualified_at"]


def find_leads(client, query, companies=5, per_company=3, seniority=None, department=None,
               log=sys.stderr):
    """Yield one row per person found.

    Discover is free; each Domain Search costs 1 credit per 10 emails returned, so with
    per_company <= 10 a run costs at most `companies` credits.
    """
    found = client.discover(query=query, limit=companies)
    for company in found[:companies]:
        domain = company.get("domain")
        if not domain:
            continue
        result = client.domain_search(domain, limit=per_company, type="personal",
                                      seniority=seniority, department=department)
        emails = result.get("emails", [])
        print(f"{domain}: {len(emails)} people", file=log)
        for e in emails:
            yield {
                "email": e.get("value", ""),
                "first_name": e.get("first_name") or "",
                "last_name": e.get("last_name") or "",
                "company": result.get("organization") or company.get("organization") or "",
                "title": e.get("position") or "",
                "website": domain,
                "linkedin_url": e.get("linkedin") or "",
                "reason": "",
                "lead_id": e.get("value", ""),
                "qualified_at": "",
            }


def write_csv(rows, out=sys.stdout):
    writer = csv.DictWriter(out, fieldnames=COLUMNS)
    writer.writeheader()
    count = 0
    for row in rows:
        writer.writerow(row)
        count += 1
    return count
