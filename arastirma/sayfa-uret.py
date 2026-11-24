"""Özgün kataloğu değiştirmeden, çevrimdışı çalışan açıklayıcı HTML üretir."""
import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from katalog_yukle import load_catalog
catalog, _ = load_catalog(root)
assert len(catalog) == 190, 'Beklenmedik katalog değişimi'
by_record = {}
for name in ('metin-ilk-tur.json', 'ses-ilk-tur.json'):
    path = root / 'arastirma' / name
    if path.exists():
        for item in json.loads(path.read_text(encoding='utf-8-sig'))['models']:
            matches=[i+1 for i,c in enumerate(catalog) if c['url'].rstrip('/').casefold()==('https://huggingface.co/'+item['id']).casefold()]
            assert len(matches)==1, item['id']
            item['record_id']=matches[0]
            by_record[matches[0]]=item
packet_ids=set()
for path in sorted((root/'arastirma/tam-tarama').glob('*-sonuc.json')):
    records=json.loads(path.read_text(encoding='utf-8-sig'))['records']
    expected=json.loads(path.with_name(path.name.replace('-sonuc.json','-girdi.json')).read_text(encoding='utf-8-sig'))
    assert {r['record_id'] for r in records}=={r['record_id'] for r in expected}, path
    assert not packet_ids.intersection(r['record_id'] for r in records), path
    packet_ids.update(r['record_id'] for r in records)
    for item in records:
        assert 1<=item['record_id']<=190, path
        by_record[item['record_id']]=item
models=[by_record[i] for i in sorted(by_record)]
revisions = json.loads((root/'arastirma/depo-kimlikleri.json').read_text(encoding='utf-8-sig'))
selection = json.loads((root/'arastirma/eleme-kararlari.json').read_text(encoding='utf-8'))
template = (root/'sayfalar/turkce-model-laboratuvari.template.html').read_text(encoding='utf-8')
for token, data in [('__CATALOG__', catalog), ('__RESEARCH__', models), ('__REVISIONS__', revisions), ('__SELECTION__', selection)]:
    template = template.replace(token, json.dumps(data, ensure_ascii=False).replace('<', r'\u003c'))
destination = root / 'sayfalar/TURKCE-MODEL-LABORATUVARI.html'
destination.write_text(template, encoding='utf-8')
print(json.dumps({'output': str(destination), 'catalog_records': len(catalog), 'research_cards': len(models)}, ensure_ascii=False))
