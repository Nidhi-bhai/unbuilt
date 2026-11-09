import json,re,datetime,collections
U=json.load(open('data/unbuilt.json')); paid=json.load(open('data/paid.json')); W=json.load(open('data/wishes.json'))
raw=sum(1 for _ in open('data/raw.jsonl'))
EXCL=re.compile(r"^(services want|services use|single subscription|subscribe|customer|really focuses|annual subscription|dollars month|subscription.*|store|free version|history|extension adds|ios app|apk)$")
C=[c for c in U['clusters'] if not EXCL.match(c['kw'][0])]
def it(w): return {'id':w['id'],'a':w['a'],'t':w['t'],'d':w['d'],'st':w.get('st','')[:120]}
clusters=[{'q':c['label'],'kw':c['kw'],'n':c['n'],'first':c['first'],'last':c['last'],'items':[it(w) for w in c['items']]} for c in C]
data={'updated':datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d'),
 'stats':{'matched':raw,'requests':len(W),'product':len(U['all']),'themes':len(clusters),'people':len({w['a'] for w in W})},
 'clusters':clusters,
 'paid':[{'sid':p['sid'],'title':p['title'],'url':p['url'],'n':p['n'],'q':p['quotes'][:5]} for p in paid if p['n']>=2][:60],
 'all':[it(w) for w in W]}
json.dump(data,open('docs/data.json','w'),separators=(',',':'))
# open dataset files
import csv
with open('docs/unbuilt-requests.csv','w',newline='') as f:
    wr=csv.writer(f); wr.writerow(['hn_id','author','date','phrase','text','story_title','hn_url'])
    for w in W: wr.writerow([w['id'],w['a'],w['d'],w['p'],w['t'],w.get('st',''),f"https://news.ycombinator.com/item?id={w['id']}"])
print(data['stats'], 'top:',[ (c['n'],c['kw'][0]) for c in clusters[:12]])
