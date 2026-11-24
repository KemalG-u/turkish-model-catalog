import json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
root=Path(__file__).resolve().parent/'tam-tarama'
for num in sys.argv[1:]:
    d=json.loads((root/'kayitlar'/f'{int(num):03}.json').read_text(encoding='utf-8'))
    body=''
    for source in d['sources']:
        cached=json.loads(Path(source['cache_file']).read_text(encoding='utf-8'))
        if cached.get('text') and ('README.md' in source['url'] or not body):body=cached['text']
    body=re.sub(r'^---\s*\n[\s\S]*?\n---\s*\n','',body)
    m=d.get('metadata',{});card=m.get('cardData') or {}
    print(json.dumps({'record_id':d['record_id'],'name':d['catalog']['ad'],'url':d['catalog']['url'],'status':d['sources'][0]['status'] if d['sources'] else None,'repo':d.get('repo_id'),'sha':m.get('sha'),'modified':m.get('lastModified'),'base':card.get('base_model'),'body':body[:2500],'community':[{'title':x['title'],'url':x['url'],'comments':[{'by':e['author'].get('name'),'text':e['content'][:800]} for e in x['events'][:3]]} for x in d['community']],'links':d.get('links',[])[:8]},ensure_ascii=False))
