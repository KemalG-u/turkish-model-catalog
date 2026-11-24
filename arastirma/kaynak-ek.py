import importlib.util,json,sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
path=Path(__file__).with_name('kaynak-topla.py')
spec=importlib.util.spec_from_file_location('public_sources',path)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
for u in sys.argv[1:]:
    r=module.fetch(u)
    print(json.dumps(module.ref(r)|{'text':r.get('text','')[:6000],'data':r.get('data') if isinstance(r.get('data'),dict) and len(str(r.get('data')))<4000 else None},ensure_ascii=False))
