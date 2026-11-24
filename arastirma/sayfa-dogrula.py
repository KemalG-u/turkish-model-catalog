"""Yerel HTML'nin veri ve sözdizimi kontrolü; tarayıcı kabulü değildir."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from katalog_yukle import load_catalog
original,src=load_catalog(root)
output=root/'sayfalar/TURKCE-MODEL-LABORATUVARI.html'
html=output.read_text(encoding='utf-8')
def extract(text, name):
    m=re.search(r'<script id="'+name+r'" type="application/json">([\s\S]*?)</script>',text)
    assert m, name
    return json.loads(m.group(1))
catalog=extract(html,'catalog-data')
cards=extract(html,'research-data')
selection=extract(html,'selection-data')
excluded={r['record_id'] for r in selection['excluded']}
replaced={r['record_id'] for r in selection['replacements']}
assert not excluded.intersection(replaced)
assert excluded.union(replaced).issubset(set(range(1,191)))
for row in selection['excluded']+selection['replacements']:
    assert row['reason'] and row['evidence']
    assert all(u.startswith(('https://','http://')) for u in row['evidence'])
assert catalog==original and len(catalog)==190
assert src is None or hashlib.sha256(src.read_bytes()).hexdigest().upper()=='A122C16DDFA5CA9DD132284A6FB552BA5FC37CA94EC064D05436D12CDF95CE66'
matched=[]
partial='--partial' in sys.argv
for card in cards:
    for field in ('id','plain','claims','training','version','try_it','independent','unknowns','sources'):
        assert field in card, (card['id'],field)
    assert isinstance(card.get('record_id'),int) and 1<=card['record_id']<=190
    matched.append(card['record_id'])
    if not partial:
        assert card.get('research_status') in ('documented','limited','identity_unresolved','non_model'),card['record_id']
        assert {x['channel'] for x in card['channels']}=={'developer','community','social_video','version'},card['record_id']
        for claim in card['claims']:
            assert claim['source'].startswith(('https://','http://')),(card['record_id'],claim)
assert len(matched)==len(set(matched))
if not partial:
    assert set(matched)==set(range(1,191)), sorted(set(range(1,191))-set(matched))
assert 'kalite puanı değildir' in html
assert 'Bu kayıttaki üyeler ve araştırma kapsamı' in html
assert 'Hangi kanallara bakıldı?' in html
assert 'Araştırma açığı olanlar' in html
assert 'Hiçbir model bu çalışmada çalıştırılmadı' in html
assert not re.search(r'<script[^>]+src=',html)
assert not re.search(r'__(CATALOG|RESEARCH|REVISIONS|SELECTION)__',html)
scripts=re.findall(r'<script(?: [^>]*)?>([\s\S]*?)</script>',html)
js=root/'arastirma/sayfa-kontrol.js'
js.write_text(scripts[-1],encoding='utf-8')
subprocess.run(['node','--check',str(js)],check=True)
search_fn=re.search(r'function searchKey\(value\)\{[^}]+\}',scripts[-1]).group(0)
subprocess.run(['node','-e',search_fn+";if(searchKey('WHISPER')!==searchKey('Whisper'))throw Error('ASCII case');if(searchKey('TÜRKÇE')!==searchKey('turkce'))throw Error('Turkish search');"],check=True)
assert 'id="page" role="status" aria-live="polite"' in html
result={'catalog_records':len(catalog),'source_cards':len(cards),'awaiting_card':len(catalog)-len(cards),'source_count':len({s['url'] for c in cards for s in c['sources']}),'research_status_counts':{k:sum(c.get('research_status')==k for c in cards) for k in ('documented','limited','identity_unresolved','non_model')},'original_unchanged':True,'javascript_syntax':'PASS','browser_visual_and_interaction':'NOT_VERIFIED: file URL navigation was blocked by browser security policy','check_date':'2026-10-23','partial':partial}
patches={r['record_id']:r['research'] for r in selection['replacements']}
active=[dict(c,**patches.get(c['record_id'],{})) for c in cards if c['record_id'] not in excluded]
result.update({'active_records':len(catalog)-len(excluded),'updated_cards':len(replaced),'removed_whole_records':len(excluded),'active_source_count':len({s['url'] for c in active for s in c['sources']})})
(root/'arastirma/dogrulama.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
