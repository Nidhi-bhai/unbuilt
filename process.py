import json,re,html,collections,datetime
PH=["i would pay for","i'd pay for","i would happily pay","i'd happily pay","i would gladly pay","i'd gladly pay","shut up and take my money","take my money","someone should build","someone please build","somebody should build","i wish there was a tool","i wish there was an app","i wish someone would build","is there a tool that","is there an app that","why is there no","i'd pay good money","i would pay good money","would pay money for"]
PAYPH=[p for p in PH if 'pay' in p or 'money' in p]
DEICTIC=re.compile(r"^(?:\s*(?:good money|money|\$?\d[\d,.]*\s*(?:usd|dollars|bucks|/mo(?:nth)?|a month|per month|/yr|a year|per year)?|real money|a subscription|a license))?\s*(?:for\s+)?(?:this|that|it|these|those|them|one|such a thing|something like (?:this|that)|a (?:service|tool|product|thing) like (?:this|that)|the (?:service|product|tool|app))\b",re.I)
TOOLY=re.compile(r"\b(tool|app|software|service|library|lib|api|website|site|saas|plugin|extension|cli|open[- ]source|alternative|product|platform|database|editor|client|framework|startup|marketplace|search engine|dashboard)\b",re.I)
def clean(t):
    t=re.sub(r'<p>',' \n',t or ''); t=re.sub(r'<[^>]+>','',t); t=html.unescape(t)
    return t.replace('\u2019',"'").replace('\u2018',"'")
def sentences(t): return [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n+',t) if s.strip()]
rows=[json.loads(l) for l in open('data/raw.jsonl')]
pay=collections.defaultdict(lambda:{'authors':set(),'quotes':[]})
wishes=[];stories={}
for h in rows:
    isstory='story' in h.get('_tags',[])
    txt=clean(h.get('comment_text') or ((h.get('title') or '')+'. '+(h.get('story_text') or '')))
    low=txt.lower()
    sid=str(h.get('story_id') or h['objectID'])
    if h.get('story_title'): stories[sid]=(h['story_title'],h.get('story_url'))
    for s in sentences(txt):
        sl=s.lower(); hit=next((p for p in PH if p in sl),None)
        if not hit: continue
        after=sl.split(hit,1)[1]
        if hit in PAYPH and (DEICTIC.match(after) or 'take my money' in hit) and not isstory and str(h.get('parent_id'))==sid and len(after.strip())<160:
            if re.search(r"\b(not|never|wouldn't|won't|no one|nobody)\b", sl.split(hit)[0][-25:]): break
            d=pay[sid]; 
            if h['author'] not in d['authors']:
                d['authors'].add(h['author']); d['quotes'].append({'a':h['author'],'id':h['objectID'],'t':s[:240],'d':h['created_at'][:10]})
            break
        words=re.findall(r"[a-z0-9']+",after)
        if len(words)<4 or DEICTIC.match(after): continue
        if hit=='why is there no' and not TOOLY.search(after): continue
        if re.search(r"\b(not|never|wouldn't|won't)\s*$", sl.split(hit)[0][-12:]): continue
        if s.endswith('?') is False and hit.startswith('is there') and False: pass
        wishes.append({'id':h['objectID'],'a':h['author'],'t':s[:300],'p':hit,'d':h['created_at'][:10],'story':sid,'st':(h.get('story_title') or h.get('title') or ''),'r':len(h.get('children') or [])})
        break
board=[]
for sid,d in pay.items():
    if sid not in stories: continue
    t,u=stories[sid]
    board.append({'sid':sid,'title':t,'url':u,'n':len(d['authors']),'quotes':sorted(d['quotes'],key=lambda q:q['d'])})
board.sort(key=lambda x:(-x['n'],x['title']))
# dedupe wishes: one per author per story
seen=set();W=[]
for w in wishes:
    k=(w['a'],w['story'])
    if k in seen: continue
    seen.add(k);W.append(w)
json.dump(board,open('data/paid.json','w')); json.dump(W,open('data/wishes.json','w'))
print('rows',len(rows),'paystories',len(board),'payvotes',sum(b['n'] for b in board),'wishes',len(W))
for b in board[:25]: print(b['n'],b['title'][:90])
import random;random.seed(1)
for w in random.sample(W,25): print('-',w['p'],'|',w['t'][:160])
