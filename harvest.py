import json,urllib.request,urllib.parse,time,datetime,sys,os
PHRASES=["i would pay for","i'd pay for","i would happily pay","i'd happily pay","i would gladly pay","i'd gladly pay","shut up and take my money","take my money","someone should build","someone please build","somebody should build","i wish there was a tool","i wish there was an app","i wish someone would build","is there a tool that","is there an app that","why is there no","i'd pay good money","i would pay good money","would pay money for"]
OUT='data/raw.jsonl'
seen=set();maxts=0
if os.path.exists(OUT):
    for l in open(OUT):
        j=json.loads(l); seen.add(j['objectID']); maxts=max(maxts,int(j.get('created_at_i',0)))
INC=os.environ.get('INCREMENTAL')=='1' and maxts>0
f=open(OUT,'a')
def get(q,tags,a,b):
    p={'query':f'"{q}"','tags':tags,'hitsPerPage':1000,'numericFilters':f'created_at_i>={a},created_at_i<{b}'}
    u='https://hn.algolia.com/api/v1/search_by_date?'+urllib.parse.urlencode(p)
    for i in range(4):
        try: return json.load(urllib.request.urlopen(u,timeout=60))
        except Exception as e: print('err',e,file=sys.stderr); time.sleep(3)
    return {'hits':[],'nbHits':0}
def slice_(q,tags,a,b,depth=0):
    d=get(q,tags,a,b); n=d['nbHits']
    if n>1000 and b-a>86400*7:
        m=(a+b)//2; return slice_(q,tags,a,m,depth+1)+slice_(q,tags,m,b,depth+1)
    c=0
    for h in d['hits']:
        if h['objectID'] in seen: continue
        seen.add(h['objectID']); h.pop('_highlightResult',None); h['_phrase']=q
        f.write(json.dumps(h)+'\n'); c+=1
    time.sleep(0.15); return c
start=int(datetime.datetime(2007,1,1).timestamp()); end=int(time.time())+86400
for q in PHRASES:
    tot=0
    if INC:
        tot+=slice_(q,'(comment,story)',maxts-3*86400,end)
    else:
      for y in range(2007,datetime.date.today().year+1):
        a=int(datetime.datetime(y,1,1).timestamp()); b=min(int(datetime.datetime(y+1,1,1).timestamp()),end)
        tot+=slice_(q,'(comment,story)',a,b)
    f.flush(); print(q,tot,flush=True)
