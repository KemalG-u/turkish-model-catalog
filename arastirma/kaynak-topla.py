"""Kamuya açık metin/metadata toplayıcı. Kimlik bilgisi, paket, ağırlık ve medya indirmez."""
import concurrent.futures as cf
import hashlib, html, json, re, sys, threading, time
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, quote, urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'arastirma/tam-tarama'; CACHE=OUT/'kaynaklar'; DOS=OUT/'kayitlar'
for p in (OUT,CACHE,DOS): p.mkdir(parents=True,exist_ok=True)
DAY='2026-10-23'
sys.path.insert(0,str(Path(__file__).resolve().parent))
from katalog_yukle import load_catalog
catalog,_=load_catalog(ROOT)
locks={}; mutex=threading.Lock()
class Plain(HTMLParser):
    def __init__(self): super().__init__(); self.skip=0; self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style','noscript'): self.skip+=1
        if tag in ('p','div','h1','h2','h3','li','tr','br'): self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag in ('script','style','noscript') and self.skip: self.skip-=1
    def handle_data(self,data):
        if not self.skip:self.parts.append(data)
def fetch(url):
    key=hashlib.sha256(url.encode()).hexdigest()[:20]
    with mutex: lock=locks.setdefault(key,threading.Lock())
    with lock:
        path=CACHE/(key+'.json')
        if path.exists(): return json.loads(path.read_text(encoding='utf-8'))
        result={'url':url,'checked_at':DAY}
        try:
            req=Request(url,headers={'User-Agent':'Turkish-Model-Catalog-Research/1.0','Accept':'application/json,text/plain,text/html'})
            with urlopen(req,timeout=22) as f:
                ct=f.headers.get('Content-Type',''); result.update(status=f.status,resolved_url=f.url,content_type=ct)
                if any(x in ct for x in ('pdf','audio/','image/','octet-stream')): result['error']='BINARY_NOT_FETCHED'
                else:
                    raw=f.read(700001); result['truncated']=len(raw)>700000
                    text=raw[:700000].decode('utf-8','replace')
                    if 'json' in ct:
                        result['data']=json.loads(text)
                    else:
                        if 'html' in ct:
                            p=Plain();p.feed(text);text=html.unescape(''.join(p.parts))
                        text=re.sub(r'[ \t]+',' ',text);text=re.sub(r'\n\s*\n+','\n\n',text)
                        result['text']=text
        except HTTPError as e: result.update(status=e.code,error=str(e))
        except Exception as e:result.update(status=0,error=str(e))
        path.write_text(json.dumps(result,ensure_ascii=False),encoding='utf-8')
        return result
def ref(r):
    key=hashlib.sha256(r['url'].encode()).hexdigest()[:20]
    return {k:r.get(k) for k in ('url','checked_at','status','resolved_url','error','truncated')}|{'cache_file':str(CACHE/(key+'.json'))}
def snippets(text):
    # Bunlar yönlendirme alıntısıdır; ajan hüküm vermeden asıl metni okuyabilir.
    sections=[]
    lines=text.splitlines()
    for i,line in enumerate(lines):
        if re.search(r'claim|train|evaluat|benchmark|result|limitation|base model|license|release|version|dataset|how.to|usage|WER|CER|MOS|Türkçe|eğitim|başarı|iddia|veri|sürüm',line,re.I):
            sections.append(' '.join(lines[max(0,i-1):i+4])[:550])
    return list(dict.fromkeys(sections))[:16]
def one(index):
    c=catalog[index];d={'record_id':index+1,'catalog':c,'checked_at':DAY,'sources':[],'metadata':{},'extracts':[],'community':[],'related_releases':[],'links':[]}
    u=c.get('url','');p=urlparse(u);parts=p.path.strip('/').split('/')
    if p.netloc=='huggingface.co' and len(parts)>=2 and parts[0] not in ('api','collections','organizations'):
        kind='models';offset=0
        if parts[0] in ('datasets','spaces'):kind=parts[0];offset=1
        if len(parts)<offset+2:return d
        rid='/'.join(parts[offset:offset+2]);d['repo_id']=rid;d['repo_kind']=kind
        api=fetch('https://huggingface.co/api/'+kind+'/'+rid);d['sources'].append(ref(api));m=api.get('data',{})
        if isinstance(m,dict):
            d['metadata']={k:m.get(k) for k in ('id','sha','createdAt','lastModified','pipeline_tag','gated','private','cardData','tags')}
        prefix='' if kind=='models' else kind+'/'
        readme=fetch('https://huggingface.co/'+prefix+rid+'/raw/main/README.md');d['sources'].append(ref(readme))
        text=readme.get('text','');d['extracts']=snippets(text);d['lead']=text[:2000]
        d['links']=list(dict.fromkeys(re.findall(r'https?://[^\s<>\[\]()"\']+',text)))[:35]
        author=rid.split('/')[0]
        profile=fetch('https://huggingface.co/'+author);d['sources'].append(ref(profile));d['profile_excerpt']=profile.get('text','')[:1000]
        if kind=='models':
            family=fetch('https://huggingface.co/api/models?'+urlencode({'author':author,'sort':'lastModified','direction':-1,'limit':40}));d['sources'].append(ref(family))
            if isinstance(family.get('data'),list):d['related_releases']=[{k:x.get(k) for k in ('id','lastModified','pipeline_tag')} for x in family['data']]
        discussions=fetch('https://huggingface.co/api/'+kind+'/'+rid+'/discussions');d['sources'].append(ref(discussions))
        threads=discussions.get('data',{});threads=threads.get('discussions',[]) if isinstance(threads,dict) else []
        d['discussion_count']=len(threads)
        chosen=[x for x in threads if not x.get('isPullRequest')][:2]
        for t in chosen:
            detail=fetch('https://huggingface.co/api/'+kind+'/'+rid+'/discussions/'+str(t.get('num')));d['sources'].append(ref(detail))
            data=detail.get('data',{});events=[]
            for e in data.get('events',[]) if isinstance(data,dict) else []:
                if e.get('type')=='comment':events.append({'author':e.get('author'),'content':str(e.get('data',{}).get('latest',{}).get('raw',e.get('content','')))[:3200]})
            d['community'].append({'num':t.get('num'),'title':t.get('title'),'author':t.get('author'),'url':'https://huggingface.co/'+prefix+rid+'/discussions/'+str(t.get('num')),'events':events})
    elif u:
        # PDF yerine resmî özet sayfası okunur; PDF indirilmez.
        target=re.sub(r'https://arxiv.org/pdf/([^/?]+)(?:\.pdf)?',lambda m:'https://arxiv.org/abs/'+m.group(1).removesuffix('.pdf'),u)
        r=fetch(target);d['sources'].append(ref(r));text=r.get('text','');d['lead']=text[:2500];d['extracts']=snippets(text)
        if isinstance(r.get('data'),list): d['api_results']=r['data'][:15]
        d['links']=list(dict.fromkeys(re.findall(r'https?://[^\s<>\[\]()"\']+',text)))[:20]
    else:d['missing_url']=True
    (DOS/f'{index+1:03}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
    return {'record_id':index+1,'name':c['ad'],'category':c['tur'],'source_status':d['sources'][0]['status'] if d['sources'] else None,'repo_id':d.get('repo_id')}
groups={}
general=[i for i,c in enumerate(catalog) if c['tur']=='LLM-genel']
groups['01-metin-a']=general[:23];groups['02-metin-b']=general[23:]
groups['03-asr']=[i for i,c in enumerate(catalog) if c['tur']=='ASR']
groups['04-tts']=[i for i,c in enumerate(catalog) if c['tur']=='TTS']
groups['05-alan']=[i for i,c in enumerate(catalog) if c['tur'].startswith('LLM-alan:')]
groups['06-nlp']=[i for i,c in enumerate(catalog) if c['tur'] in ('Kodlayıcı-BERT','Gömme/reranker','NER-PII','Noktalama-yazım-morfoloji','Çeviri')]
rest=[i for i in range(len(catalog)) if not any(i in ids for ids in groups.values())]
groups['07-kaynak-a']=rest[:20];groups['08-kaynak-b']=rest[20:]
for name,ids in groups.items():
    batch=[{'record_id':i+1,'name':catalog[i]['ad'],'category':catalog[i]['tur'],'url':catalog[i]['url'],'dossier':str(DOS/f'{i+1:03}.json')} for i in ids]
    (OUT/(name+'-girdi.json')).write_text(json.dumps(batch,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':
    with cf.ThreadPoolExecutor(max_workers=6) as pool:
        results=list(pool.map(one,range(len(catalog))))
    (OUT/'toplama-ozeti.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'records':len(results),'fetched_ok':sum(r['source_status']==200 for r in results),'batches':{k:len(v) for k,v in groups.items()}},ensure_ascii=False),flush=True)
