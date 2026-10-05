from pathlib import Path
import datetime,json,urllib.request,concurrent.futures
ROOT=Path(__file__).resolve().parent
cfg={}
for line in (ROOT.parents[1]/'.env').read_text().splitlines():
 if line.strip() and not line.lstrip().startswith('#') and '=' in line:
  k,v=line.split('=',1);cfg[k.strip()]=v.strip().strip('\"').strip("'")
headers={'X-NCP-APIGW-API-KEY-ID':cfg['NAVER_CLIENT_KEY'],'X-NCP-APIGW-API-KEY':cfg['NAVER_SECRET'],'Content-Type':'application/json'}
groups=[{'groupName':q,'keywords':[q]} for q in ['압구정 소개팅','압구정 데이트','압구정 데이트코스']]
tasks=[('last30days','2026-08-21','2026-09-19','date'),('last12months','2025-09-01','2026-08-31','month')]
def run(t):
 name,start,end,unit=t;p={'startDate':start,'endDate':end,'timeUnit':unit,'keywordGroups':groups}
 rec={'name':name,'params':p,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request('https://naverapihub.apigw.ntruss.com/search-trend/v1/search',data=json.dumps(p).encode(),headers=headers)
  with urllib.request.urlopen(req,timeout=30) as r:rec.update(status=r.status,response=json.load(r))
 except Exception as e:rec.update(status='error',error=type(e).__name__)
 return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rs=list(pool.map(run,tasks))
(ROOT/'keyword-comparison.json').write_text(json.dumps(rs,ensure_ascii=False,indent=2))
for r in rs:
 print(json.dumps(r,ensure_ascii=False))
