"""Collect NAVER blog-search and trend evidence without saving API credentials."""
from pathlib import Path
import concurrent.futures
import datetime
import json
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent
cfg = {}
for line in (ROOT.parents[1] / ".env").read_text().splitlines():
    if line.strip() and not line.lstrip().startswith("#") and "=" in line:
        key, value = line.split("=", 1)
        cfg[key.strip()] = value.strip().strip('"').strip("'")

headers = {
    "X-NCP-APIGW-API-KEY-ID": cfg["NAVER_CLIENT_KEY"],
    "X-NCP-APIGW-API-KEY": cfg["NAVER_SECRET"],
}
base = "https://naverapihub.apigw.ntruss.com"
queries = [
    "문래동 영일분식",
    "영일분식 비빔칼국수",
    "문래동 비빔칼국수",
    "영등포 맛집",
    "영일분식 만두",
]


def call(task):
    name, path, params, method = task
    body = json.dumps(params).encode() if method == "POST" else None
    url = base + path + ("?" + urllib.parse.urlencode(params) if method == "GET" else "")
    request_headers = dict(headers)
    if body:
        request_headers["Content-Type"] = "application/json"
    record = {
        "name": name,
        "endpoint": path,
        "params": params,
        "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    try:
        request = urllib.request.Request(url, data=body, headers=request_headers, method=method)
        with urllib.request.urlopen(request, timeout=30) as response:
            record.update(status=response.status, response=json.load(response))
    except urllib.error.HTTPError as error:
        record.update(status=error.code, error=error.read().decode()[:500])
    except Exception as error:
        record.update(status="error", error=type(error).__name__)
    return record


end = datetime.date(2026, 9, 28)
groups = [{"groupName": query, "keywords": [query]} for query in queries]
tasks = [
    (query + "_" + sort, "/search/v1/blog", {"query": query, "display": 20, "sort": sort}, "GET")
    for query in queries
    for sort in ["sim", "date"]
]
for weeks in [52, 8]:
    tasks.append(
        (
            "trend_" + str(weeks) + "w",
            "/search-trend/v1/search",
            {
                "startDate": str(end - datetime.timedelta(weeks=weeks) + datetime.timedelta(days=1)),
                "endDate": str(end),
                "timeUnit": "week",
                "keywordGroups": groups,
            },
            "POST",
        )
    )

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    records = list(pool.map(call, tasks))

(ROOT / "naver-api-results.json").write_text(json.dumps(records, ensure_ascii=False, indent=2))
for record in records:
    data = record.get("response", {})
    print(record["name"], "status", record["status"], "total", data.get("total", ""))
    for result in data.get("results", []):
        print("TREND", result["title"], "points", len(result["data"]))
