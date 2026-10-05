"""Collect NAVER search/trend evidence without saving API credentials."""
from pathlib import Path
import concurrent.futures, datetime, html, json, re, urllib.request, urllib.parse, urllib.error
ROOT = Path(__file__).resolve().parent
cfg = {}
for line in (ROOT.parents[1] / '.env').read_text().splitlines():
    if line.strip() and not line.lstrip().startswith('#') and '=' in line:
        key, value = line.split('=', 1)
        cfg[key.strip()] = value.strip().strip('"').strip("'")
headers = {'X-NCP-APIGW-API-KEY-ID': cfg['NAVER_CLIENT_KEY'], 'X-NCP-APIGW-API-KEY': cfg['NAVER_SECRET']}
base = 'https://naverapihub.apigw.ntruss.com'
queries = ['노량진 생새우', '노량진 생새우 가격', '노량진 생새우 초장집', '노량진 생새우 손질', '노량진 전라도 초장집', '노량진 생새우 1kg', '노량진 생새우 웨이팅']
def call(task):
    name, path, params, method = task
    body = json.dumps(params).encode() if method == 'POST' else None
    url = base + path + ('?' + urllib.parse.urlencode(params) if method == 'GET' else '')
    h = dict(headers)
    if body: h['Content-Type'] = 'application/json'
    record = {'name': name, 'endpoint': path, 'params': params, 'retrieved_at': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=body, headers=h, method=method), timeout=30) as response:
            record.update(status=response.status, response=json.load(response))
    except urllib.error.HTTPError as error:
        record.update(status=error.code, error=error.read().decode()[:500])
    except Exception as error:
        record.update(status='error', error=type(error).__name__)
    return record
end = datetime.date(2026, 9, 11)
groups = [
    {'groupName': '노량진 생새우', 'keywords': ['노량진 생새우', '노량진생새우']},
    {'groupName': '노량진 생새우 가격', 'keywords': ['노량진 생새우 가격', '노량진 생새우 시세']},
    {'groupName': '노량진 생새우 초장집', 'keywords': ['노량진 생새우 초장집']},
    {'groupName': '노량진 생새우 손질', 'keywords': ['노량진 생새우 손질', '노량진 생새우 까기']},
    {'groupName': '노량진 전라도 초장집', 'keywords': ['노량진 전라도', '노량진 전라도 초장집']},
]
tasks = [(q+'_'+sort, '/search/v1/blog', {'query':q,'display':20,'sort':sort,'format':'json'}, 'GET') for q in queries for sort in ['sim','date']]
for weeks in [52,8]:
    tasks.append(('trend_'+str(weeks)+'w', '/search-trend/v1/search', {'startDate':str(end-datetime.timedelta(weeks=weeks)+datetime.timedelta(days=1)), 'endDate':str(end),'timeUnit':'week','keywordGroups':groups}, 'POST'))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    records = list(pool.map(call,tasks))
(ROOT/'naver-api-results.json').write_text(json.dumps(records, ensure_ascii=False, indent=2))
for rec in records:
    data=rec.get('response',{})
    print(rec['name'], 'status',rec['status'],'total',data.get('total',''))
    if 'results' in data:
        for g in data['results']:
            print('TREND',g['title'],json.dumps(g['data'],ensure_ascii=False))
    else:
        items=data.get('items',[])
        relevant=[i for i in items if '노량진' in html.unescape(re.sub('<[^>]+>','',i['title'])) and any(w in html.unescape(re.sub('<[^>]+>','',i['title'])) for w in ['새우','전라도'])]
        print('Relevant titles',len(relevant),'/',len(items))
        for item in relevant[:4]: print(json.dumps(item,ensure_ascii=False))
        if 'error' in rec: print(rec['error'])
