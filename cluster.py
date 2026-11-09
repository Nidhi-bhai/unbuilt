import json,re,os,collections,numpy as np,sys
os.environ.setdefault("FASTEMBED_CACHE_PATH","/tmp/fastembed_cache")
from fastembed import TextEmbedding
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer
W=json.load(open('data/wishes.json'))
TOOLY=re.compile(r"\b(tool|tools|app|apps|software|service|services|library|api|website|site|saas|plugin|extension|cli|open[- ]source|alternative|product|platform|database|editor|client|framework|dashboard|version|tier|subscription|feature|device|reader|bot|integration|game|keyboard|laptop|phone|search|browser|ide|os|linux|emacs|vim|github|email|calendar|notes?|password|backup|hosting|vpn|music|podcast|news|feed|rss|ai|llm|model|gpt|chatgpt|course|book)\b",re.I)
NOISE=re.compile(r"\b(tax|taxes|healthcare|politic|government|police|vote|election|war|immigra|rent|salary|wage|restroom|toilet|airline|ticket|pilot)\b",re.I)
P=[w for w in W if TOOLY.search(w['t'].split(w['p'],1)[-1] if w['p'] in w['t'].lower() else w['t']) and not NOISE.search(w['t'])]
print(len(W),'->',len(P))
def strip(w):
    t=w['t']; i=t.lower().find(w['p']); return t[i+len(w['p']):] if i>=0 else t
texts=[strip(w) for w in P]
E=np.array(list(TextEmbedding("BAAI/bge-small-en-v1.5").embed(texts)))
E/=np.linalg.norm(E,axis=1,keepdims=True)
thr=float(sys.argv[1]) if len(sys.argv)>1 else 0.22
lab=AgglomerativeClustering(n_clusters=None,distance_threshold=thr,metric='cosine',linkage='average').fit_predict(E)
groups=collections.defaultdict(list)
for i,l in enumerate(lab): groups[l].append(i)
tf=TfidfVectorizer(stop_words='english',ngram_range=(1,2),min_df=2).fit(texts)
GENERIC={'service','services','app','apps','subscription','month','monthly','year','fee','pay','use','want','like','just','did','does','good','better','version','tool','product','price','money','monthly subscription','annual','mo','free','premium','dollars','buck','bucks','really','would','gladly','happily','people','thing','things','way','make','need','new','work','time','great','quality','decent','single'}
out=[]
for l,ix in groups.items():
    auth={P[i]['a'] for i in ix}
    if len(auth)<3: continue
    deic=sum(bool(re.search(r"\b(this|these|such|like that|did that|does that|something like)\b",texts[i].lower())) for i in ix)/len(ix)
    if deic>0.4: continue
    c=E[ix].mean(0); best=max(ix,key=lambda i:E[i]@c)
    v=np.asarray(tf.transform([' '.join(texts[i] for i in ix)]).todense())[0]
    names=tf.get_feature_names_out()
    kw=[names[j] for j in v.argsort()[::-1][:12] if names[j] not in GENERIC and not re.fullmatch(r'[\d\s]+|\d+ \w+|\w+ \d+',names[j])][:4]
    if not kw: continue
    title=kw[0]
    for k in kw[:3]:
        if ' ' in k and title in k: title=k

    items=sorted([P[i] for i in ix],key=lambda w:w['d'],reverse=True)
    out.append({'title':title,'label':P[best]['t'],'kw':kw,'n':len(auth),'first':min(w['d'] for w in items),'last':max(w['d'] for w in items),'items':items})
out.sort(key=lambda x:-x['n'])
json.dump({'clusters':out,'all':P},open('data/unbuilt.json','w'))
print('clusters>=3',len(out))
for o in out[:40]: print(o['n'],o['title'],o['first'][:4],o['last'][:4],o['kw'],'|',o['label'][:110])
