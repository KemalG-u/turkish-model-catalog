import concurrent.futures as cf,importlib.util,json,sys
from pathlib import Path
path=Path(__file__).with_name('kaynak-topla.py');spec=importlib.util.spec_from_file_location('sources',path);s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
extra={
107:['https://huggingface.co/Ba2han/Liquid-Turkish-MiniOCR-V0.2/raw/main/README.md','https://huggingface.co/api/models/Ba2han/Liquid-Turkish-MiniOCR-V0.2','https://huggingface.co/Trendyol/Trendyol-Vision-Flash/raw/main/README.md','https://huggingface.co/api/models/Trendyol/Trendyol-Vision-Flash','https://huggingface.co/Trendyol/Trendyol-Vision-Master/raw/main/README.md','https://huggingface.co/selimc/turkish-colpali/raw/main/README.md','https://huggingface.co/turgutguvercin/pix2struct-turkish-receipts/raw/main/README.md','https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html'],
108:['https://huggingface.co/kranidiotis/ottoman-ocr-qwen2.5-vl-7b/raw/main/README.md','https://huggingface.co/bilirkesi/osmanlica-v1/raw/main/README.md'],
109:['https://docs.livekit.io/agents/logic/turns/turn-detector/','https://livekit.com/blog/solving-end-of-turn-detection','https://huggingface.co/SeaBenSea/hubert-large-turkish-speech-emotion-recognition/raw/main/README.md','https://huggingface.co/speechbrain/lang-id-voxlingua107-ecapa/raw/main/README.md'],
110:['https://community.mozilladatacollective.com/'],
111:['https://issai.nu.edu.kz/ru/turkic-asr-rus/','https://huggingface.co/datasets/issai/Turkish_Speech_Corpus/raw/main/README.md','https://huggingface.co/api/datasets/issai/Turkish_Speech_Corpus'],
112:['https://api.github.com/repos/NTRLab/MediaSpeech'],
122:['https://www.e-cloud.web.tr/project/turkmorfbench','https://huggingface.co/collections/boun-tabilab/tabibench'],
115:['https://huggingface.co/datasets/ytu-ce-cosmos/Cosmos-Turkish-Corpus-v1.0/raw/main/README.md','https://huggingface.co/api/datasets/ytu-ce-cosmos/Cosmos-Turkish-Corpus-v1.0'],
116:['https://huggingface.co/datasets/boun-tabilab/turkish_parliamentary_data/raw/main/README.md','https://huggingface.co/api/datasets/boun-tabilab/turkish_parliamentary_data'],
117:['https://raw.githubusercontent.com/GGLAB-KU/gecturk/main/README.md','https://api.github.com/repos/GGLAB-KU/gecturk','https://api.github.com/repos/GGLAB-KU/gecturk/issues?state=all&per_page=5'],
119:['https://raw.githubusercontent.com/KUIS-AI/cetvel/main/README.md','https://api.github.com/repos/KUIS-AI/cetvel'],
125:['https://arxiv.org/abs/2502.11572'],
126:['https://raw.githubusercontent.com/kesimeg/awesome-turkish-language-models/main/README.md','https://api.github.com/repos/kesimeg/awesome-turkish-language-models'],
146:['https://huggingface.co/api/datasets?author=BILGEM-AI&sort=lastModified&direction=-1&limit=20'],
166:['https://www.mdpi.com/2079-9292/12/8/1900'],
176:['https://arxiv.org/abs/2506.14190'],
177:['https://arxiv.org/abs/2409.09554'],
178:['https://aclanthology.org/W18-6115/'],
179:['https://journals.tubitak.gov.tr/elektrik/vol30/iss5/15/'],
182:['https://github.com/ArdaYuksel/TurkishMMLU'],
185:['https://github.com/ezgibasar/TurBLiMP','https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/turblimp/README.md']}
urls=sorted({u for v in extra.values() for u in v})
with cf.ThreadPoolExecutor(max_workers=5) as pool:results=dict(zip(urls,pool.map(s.fetch,urls)))
out={str(i):[s.ref(results[u]) for u in urls] for i,urls in extra.items()}
(s.OUT/'destek-ek-kaynaklar.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
for i in (() if '--quiet' in sys.argv else (107,111,115,116,117,146)):
    for r in out[str(i)]:
        x=results[r['url']];d=x.get('data');text=x.get('text','')
        if i==107:
            import re
            text=re.sub(r'^---\s*\n[\s\S]*?\n---\s*\n','',text)
        data=({k:d.get(k) for k in ('id','sha','lastModified','default_branch','pushed_at')} if isinstance(d,dict) else [{'id':a.get('id'),'title':a.get('title'),'body':str(a.get('body',''))[:700]} for a in d[:5]] if isinstance(d,list) else None)
        print(json.dumps({'record_id':i,'url':r['url'],'status':r['status'],'text':text[:1800],'data':data},ensure_ascii=True))
