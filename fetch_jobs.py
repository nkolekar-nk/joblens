import html
import os
import re
import requests

COMPANIES = [
    # AI Engineer search
    "radixexperienced", "privateequityinsights", "thesiscareers", "onestream",
    "hotmartcareersbr", "yipitdata", "simpletechnologysolutions", "addepar1", "purestorage",
    # Machine Learning Engineer search
    "pathrobotics", "pingidentity", "reolink", "cognite", "bettyjobboard",
    "checkr", "SimpliSafe", "telnyx54", "impact",
    # LLM search
    "tensordyne", "binance", "quberesearchandtechnologies",
    "asg", "authenticx", "tensorops",
    # AI Intern search
    "datacor", "eqtcorporation", "hackerrank", "schonfeld", "opensesame",
    "knowbe4", "samsungsemiconductor", "drivewealth",
]

AI_TITLE = re.compile(
    r"\b(AI|ML|Machine Learning| LLM| GenAI| Generative | NLP| Data Scien\w*| Applied Scien\w*)\b", re.I)
INTERN = re.compile(r"bintern(ship)?\b", re.I)
TECH = re.compile(r"\b(engineer\w*|software| data| developer| scien\w*)\b", re.I)
MAX_PER_COMPANY = 8

def is_relevant(title):
    # Keep AI/ML roles, plus interns only if the internship is technical
    return bool(AI_TITLE.search(title) or (INTERN.search(title) and TECH.search(title)))

os.makedirs("jobs", exist_ok=True)
report = []

for token in COMPANIES:
    url = f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs"
    try:
        resp = requests.get(url, params={"content": "true"}, timeout=20)
    except requests.RequestException as e:
        report.append((token, f"HTTP {resp.status_code}", 0, 0))
        continue
    if resp.status_code !=200:
        report.append((token, f"HTTP {resp.status_code}", 0, 0))
        continue

    jobs = resp.json().get("jobs", [])
    kept = 0
    for job in jobs:
        if kept>=MAX_PER_COMPANY:
            break
        if not is_relevant(job["title"]):
            continue
        body = html.unescape(job.get("content") or "")
        body = re.sub(r"<[^>]+>", " ", body)
        body = re.sub(r"\s+", " ", body).strip()
        if len(body)<300:                        # skip empty or near-empty postings
            continue

        header = (f"Company: {token}\nTitle: {job['title']}\n"
                  f"Location: {job['location']['name']}\nURL: {job['absolute_url']}\n\n")
        with open(f"jobs/{token}_{job['id']}.txt", "w", encoding="utf-8") as f:
            f.write(header + body)
        kept += 1
    report.append((token, "ok", len(jobs), kept))

print(f"\n{'Company':32} {'Status':10} {'Total':>6} {'Saved':>6}")
for token, status, total, kept in report:
    print(f"{token:32} {status:10} {total:>6} {kept:>6}")
print(f"\nTotal saved: {sum(r[3] for r in report)}")