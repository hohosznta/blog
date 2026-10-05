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
queries = ['가로수길 디어', '가로수길 칵테일바 디어', '신사 디어 시그니처 칵테일', '디어 칵테일 가격', '가로수길 칵테일 데이트']
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
end = datetime.date(2026, 9, 19)
groups = [{'groupName': q, 'keywords': [q]} for q in queries]
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
        for g in data['results']: print('TREND',g['title'],'points',len(g['data']))
    else:
        for item in data.get('items',[])[:3]: print(json.dumps(item,ensure_ascii=False))
