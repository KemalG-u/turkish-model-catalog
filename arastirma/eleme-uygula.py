"""Onaylanmış eleme ölçütünü etkin sayfaya uygular; kaynak arşivini korur."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
cards={}
for p in sorted((ROOT/'arastirma/tam-tarama').glob('*-sonuc.json')):
    cards.update({r['record_id']:r for r in json.loads(p.read_text(encoding='utf-8'))['records']})
selection={'checked_at':'2026-10-23','policy':'Terk edilmiş, geri çekilmiş veya kullanılabilir erişimi kalmamış adayları çıkar; devamı varsa güncel sürümü göster. Yorum eksikliği tek başına eleme nedeni değildir.','excluded':[], 'replacements':[]}

def replace(i,name,reason,evidence,patch):
    if i not in cards:return
    selection['replacements'].append({'record_id':i,'reason':reason,'evidence':evidence,'catalog':{'ad':name},'research':patch,'hide_legacy':True})

def source(u,title):
    return {'url':u,'title':title,'type':'birincil','date':None,'checked_at':'2026-10-23','status':'read'}

def channels(dev,version,note):
    return [
      {'channel':'developer','status':'checked','note':note,'urls':dev},
      {'channel':'community','status':'searched_not_found','note':'Aile araştırması bu güncel üye için girdisi ve sürümü belli bağımsız kalite deneyi doğrulamadı. Yorum eksikliği eleme nedeni sayılmadı.','urls':[]},
      {'channel':'social_video','status':'searched_not_found','note':'Aile ve geliştirici tarandı; bu güncel üye için doğrulanmış bağımsız video deneyi yok. Video izlenmedi.','urls':[]},
      {'channel':'version','status':'checked','note':version,'urls':dev}]

u='https://huggingface.co/rhasspy/piper-voices/raw/main/tr/tr_TR/dfki/medium/MODEL_CARD'
v='DFKI medium Türkçe kartına erişildi. Depo üst sürümü tek bir sesin yeni eğitimi sayılmaz; diğer erişilebilir üyelerin sürüm incelemesi açık.'
replace(67,'Piper Türkçe sesleri · DFKI ve diğer adaylar','Fahrettin/Fettah resmî kaynaktan katkıcı talebiyle kaldırılmış; bunlar çıkarıldı, erişilebilir DFKI üyesi korundu.',['https://huggingface.co/rhasspy/piper-voices/commit/b145f2ac26522d6a2ccde0164b7b0e48b1e3199c'],{
 'name':'Piper Türkçe sesleri · DFKI medium ve diğer adaylar',
 'plain':'Piper için erişilebilir Türkçe DFKI medium ses kartı var. Tek konuşmacı ve 22.050 Hz çıkış bildiriyor. Diğer adayların dosya, lisans ve kalite bilgileri ayrıca incelenmeli; hepsi aynı ses değildir.',
 'training':'DFKI medium, İngilizce lessac sesinden ince ayarlı. Veri kartı CC BY-NC-SA 4.0 gösteriyor; depo üst lisans etiketi her sesin koşullarını tek başına çözmez.',
 'version':v,'revision':None,
 'try_it':'Piper motoru ve DFKI medium ses dosyasıyla yerel kullanım yolu var. MODEL_CARD, veri ve lisans bağlantısını veriyor. Bu çalışmada ses dosyası indirilmedi veya denenmedi.',
 'independent':'Aileye ait eski uygulama yorumları DFKI sesinin kalite kanıtı sayılmadı. DFKI için girdisi ve sürümü belli bağımsız dinleme karşılaştırması doğrulanmadı.',
 'unknowns':['99eren99, dcx514ai, Cem ve diğer adayların ayrı güncel dosya, lisans ve kalite incelemesi açık.','DFKI için insan dinlemesi, sayı telaffuzu ve hız henüz ölçülmedi.'],
 'members':[{'name':'rhasspy DFKI medium','url':u,'status':'Türkçe MODEL_CARD okundu; model çalıştırılmadı.'},{'name':'99eren99, dcx514ai, Cem ve diğer adaylar','url':None,'status':'Ayrı dosya/kimlik/lisans incelemesi açık; kaliteleri doğrulanmış sayılmaz.'}],
 'sources':[source(u,'Piper DFKI medium Türkçe ses kartı')], 'channels':channels([u],v,'Erişilebilir DFKI medium kartı okundu; kaldırılmış seslerin kullanıcı yorumları bu üyeye taşınmadı.')})

u='https://huggingface.co/cloud0day3/antalia-mini/raw/main/README.md'
v='Antalia-2 Mini 1.0.1; 7,62 milyon parametre, 48 kHz. Resmî kartın gösterdiği sürüm; dosya tarihi yeni eğitim tarihi sayılmadı.'
replace(73,'Antalia-2 Mini · 1.0.1','Geliştirmenin durduğu resmî olarak açıklanan Antalia-1 yerine erişilebilir Antalia-2 Mini gösterildi.',['https://huggingface.co/cloud0day3/antalia-1/raw/main/README.md',u],{
 'id':'cloud0day3/antalia-mini','name':'Antalia-2 Mini 1.0.1','kind':'model','creator':'cloud0day3 / Patientdesk AI',
 'plain':'Küçük, tek sentetik erkek sesli Türkçe metinden konuşmaya modelidir. Geliştirici, işlemcide gerçek zamandan hızlı çalıştığını ve sayı, tarih, tutar ile kısaltmaları okunuşa çevirdiğini söylüyor.',
 'claims':[{'text':'7,62 milyon parametreyle 48 kHz konuşma üretimi ve işlemcide gerçek zamandan hızlı kullanım hedefleniyor.','evidence':'Geliştirici beyanı; bu bilgisayarda ölçülmedi.','source':u},{'text':'Sayı, tarih, saat, tutar, kısaltma ve bazı yabancı adları okunuşa çeviren bir normalleştirici içeriyor.','evidence':'Resmî kartın işlev tarifi; her girdide doğru çalışma kanıtı değil.','source':u}],
 'training':'Kart, eğitim verisinde gerçek konuşmacı kaydı olmadığını; sesin sentetik olduğunu ve kod/ağırlıkların Apache-2.0 lisansıyla yayımlandığını söylüyor.',
 'version':v,'revision':None,'demo_url':'https://huggingface.co/spaces/cloud0day3/antalia-mini',
 'try_it':'Hazır tarayıcı demosu bağlantısı ve Python paketi var. Geliştirici, demonun cihazda ONNX Runtime Web ile çalıştığını söylüyor. Demo/model çalıştırılmadı; paket kurulmadı.',
 'independent':'Güncel Mini için sürümü ve girdisi belli bağımsız dinleyici karşılaştırması bu taramada doğrulanmadı.',
 'unknowns':['Türkçe telaffuz, doğallık, uzun metin ve hız bu laboratuvarda ölçülmedi.','Kartın baştaki ö/ı ve çift sesler için anlattığı düzeltmeler gerçek örneklerle sınanmalı.'],
 'members':[{'name':'cloud0day3/antalia-mini','url':'https://huggingface.co/cloud0day3/antalia-mini','status':'1.0.1 kartı okundu; ses üretilmedi.'}],
 'sources':[source(u,'Antalia-2 Mini 1.0.1 resmî kartı')], 'channels':channels([u],v,'Antalia-2 Mini kartı okundu; önceki modelin puanı bu sürüme aktarılmadı.')})

if 109 in cards:
    r=cards[109];u='https://livekit.com/blog/solving-end-of-turn-detection';docs='https://docs.livekit.io/agents/logic/turns/turn-detector/'
    v='LiveKit resmî 17 Haziran 2026 duyurusu v1/v1-mini ses ve anlam bileşimini anlatıyor. Diğer ses sınıflayıcılarının sürümleri ayrı; eski metin modeli puanı bu sürüme taşınmadı.'
    replace(109,'Ses sınıflandırıcıları ve LiveKit Turn Detector v1','Kullanımdan kaldırılan İngilizce varyant yerine güncel çok dilli v1 yolu gösterildi. Eski Türkçe kullanıcı yorumu yeni v1 kalitesi sayılmadı.',['https://docs.livekit.io/agents/logic/turns/turn-detector/',u],{
      'name':'Ses sınıflandırıcıları ve LiveKit Turn Detector v1',
      'plain':'Konuşmanın bittiğini bulma, dili tanıma ve duyguyu sınıflama farklı görevlerdir. LiveKit v1, ses ve anlamı birlikte kullanarak sıra sonunu tahmin eder; resmî duyuruda Türkçe dahil 14 dil belirtiliyor.',
      'claims':[x for x in r['claims'] if x['source']==u],
      'training':'Güncel LiveKit v1 duyurusu ses kodlayıcısı ve anlam bileşimini açıklıyor. HuBERT duygu ve SpeechBrain dil sınıflayıcıları ayrı model ve eğitimlere sahip.',
      'version':v,'revision':None,
      'try_it':'LiveKit Agents güncel turn detector bütünleştirme belgesi var. Duygu ve dil tanıma için her sınıflayıcının kendi girdi/kod yolunu kullanmak gerekir. Bu modeller burada çalıştırılmadı.',
      'independent':'Eski metin tabanlı sürüme ait Türkçe kullanıcı karşılaştırması güncel v1 sonucu sayılmadı. v1 için kontrollü bağımsız Türkçe test bu taramada doğrulanmadı.',
      'unknowns':['v1 için Türkçe sıra sonu doğruluğu ve gecikme aynı seslerle ölçülmeli.','Birleşik satırdaki her duygu/dil sınıflayıcı ayrı görev olarak denenmeli.'],
      'sources':[x for x in r['sources'] if 'livekit/turn-detector' not in x['url']],
      'members':[x for x in r['members'] if 'livekit' not in x['name'].lower()]+[{'name':'LiveKit Turn Detector v1/v1-mini','url':docs,'status':'Güncel resmî belge ve duyuru okundu; denenmedi.'}],
      'channels':channels([docs,u],v,'Güncel v1 dokümanı ve blog duyurusu; eski İngilizce varyant aday listesine alınmadı.')})

u='https://raw.githubusercontent.com/coltekin/TRmorph/master/README.md'
v='TRmorph resmî deposunun xfst/foma kolu. İncelenen depo arşivli değil; eski README içindeki geliştirme ifadesi 2026 faaliyeti kanıtı sayılmadı.'
replace(98,'TRmorph · Türkçe kök ve ek çözümleme','Arşivlenmiş Google Turkish Morphology ve artık geliştirilmeyen eski SFST sürümü etkin kapsamdan çıkarıldı; erişilebilir TRmorph xfst/foma kolu korundu.',['https://github.com/google-research/turkish-morphology',u],{
 'id':'coltekin/TRmorph','name':'TRmorph · xfst/foma kolu','kind':'tool','creator':'Çağrı Çöltekin ve katkıcılar',
 'plain':'Türkçe sözcükleri kök ve eklerine çözümleyen kurallı bir araçtır. Hazır sohbet modeli veya eğitilmiş ses modeli değildir; metin işleme hattında kullanılabilir.',
 'claims':[{'text':'Türkçe biçimbilim çözümlemesi yanında kök bulma, bölümleme ve bilinmeyen sözcük işlemleri için araçlar sunuyor.','evidence':'Resmî README işlev tarifi; doğruluğu burada ölçülmedi.','source':u}],
 'training':'xfst/lexc ile tanımlanan kurallar ve foma kullanan sonlu durum yaklaşımı; büyük dil modeli ince ayarı değildir. Depoda MIT lisansı var.',
 'version':v,'revision':'fbceb1133fbdc51bd63693d448b7cb75672e2256',
 'try_it':'Resmî deponun foma ve derleme yönergeleriyle yerel kullanım yolu var. Bu oturumda kurulmadı veya çalıştırılmadı.',
 'independent':'Bu tarama güncel kol için girdisi ve sürümü belli bağımsız karşılaştırma doğrulamadı. Eski yayın/araç atfı güncel kalite kabulü sayılmadı.',
 'demo_url':None,'unknowns':['Yeni sözcükler ve günlük yazım hatalarıyla kapsama testi yapılmalı.','Depo erişimi, 2026 içinde aktif bakım yapıldığı anlamına gelmez.'],
 'members':[{'name':'TRmorph xfst/foma','url':'https://github.com/coltekin/TRmorph','status':'Resmî README ve depo metadata kaydı okundu; çalıştırılmadı.'}],
 'sources':[source(u,'TRmorph resmî README'),source('https://api.github.com/repos/coltekin/TRmorph','TRmorph depo ve arşiv durumu')],
 'channels':channels([u],v,'Korunan xfst/foma kolunun resmî README dosyası okundu. Eski sürümle karıştırılmadı.')})

u='https://huggingface.co/SykoSLM/SykoLLM-V6.9-SFT/raw/main/README.md'
v='V6.9-SFT model kartı ve kamu sürüm metadata kaydı kontrol edildi. Ağırlık hash: 401c951913ac7a4d2856795ee222065619e6b88f; dosya değişimi 11 Temmuz 2026. GGUF dönüşüm tarihi yeni eğitim sayılmadı.'
replace(140,'SykoLLM · V6.9-SFT','Eski V3.2 ana kartı yerine aynı geliştiricinin erişilebilir V6.9-SFT kartı ayrıca okunarak gösterildi. Güncel olması üstünlük kanıtı sayılmadı.',['https://huggingface.co/api/models/SykoSLM/SykoLLM-V6.9-SFT',u],{
 'id':'SykoSLM/SykoLLM-V6.9-SFT','name':'SykoLLM-V6.9-SFT','kind':'model',
 'plain':'Küçük bir metin üretme modeli. Geliştirici, V6.9 tabanına talimat örnekleriyle LoRA ince ayarı yapıp ağırlıkları birleştirdiğini açıklıyor. Uzun bağlam ve karmaşık akıl yürütme sınırlarını da belirtiyor.',
 'claims':[{'text':'Talimat izleme için yaklaşık 416 milyon parametreli modelin 24,4 milyon LoRA parametresi eğitilmiş ve tabana birleştirilmiş.','evidence':'Geliştirici eğitim tarifi; bağımsız üstünlük puanı yayımlanmış sayılmadı.','source':u}],
 'training':'SykoSLM/SykoLLM-v6.9 üzerine Alpaca biçimli talimat verisiyle LoRA; veri kümesinin tam içeriği açıklanmıyor. Kart Apache-2.0 etiketinin varsayılan olduğunu ve taban lisansının ayrıca denetlenmesini söylüyor.',
 'version':v,'revision':'401c951913ac7a4d2856795ee222065619e6b88f',
 'try_it':'Resmî kartta Transformers kullanım örneği var; yayımlanan ağırlıklar birleştirilmiş olduğundan ayrı adaptör gerektirmediği açıklanıyor. İleride aynı V6.9 tabanıyla kıyaslanabilir; bu oturumda çalıştırılmadı.',
 'demo_url':None,'independent':'Eski V3.2 yorumları V6.9 başarısına aktarılmadı. Bu güncel üye için yeniden üretilebilir bağımsız Türkçe görev karşılaştırması doğrulanmadı.',
 'unknowns':['Tam eğitim verisi ve taban lisansı netleştirilmeli.','Kartın bildirdiği 1.024 konum sınırı uzun metinde sınanmalı.'],
 'members':[{'name':'SykoLLM-V6.9-SFT','url':'https://huggingface.co/SykoSLM/SykoLLM-V6.9-SFT','status':'Güncel kart ve API okundu; denenmedi.'},{'name':'SykoLLM-v6.9 taban','url':'https://huggingface.co/SykoSLM/SykoLLM-v6.9','status':'SFT kartının bildirdiği ata; ayrı taban kartı/lisans incelemesi açık.'}],
 'sources':[source(u,'SykoLLM-V6.9-SFT resmî eğitim ve kullanım kartı'),source('https://huggingface.co/api/models/SykoSLM/SykoLLM-V6.9-SFT','V6.9-SFT sürüm metadata kaydı')],
 'channels':channels([u],v,'Eski üye yerine V6.9-SFT kartı ayrıca okundu; kalite puanı aktarılmadı.')})

if 106 in cards:
    r=cards[106];u='https://huggingface.co/tencent/Hy-MT2-1.8B/raw/main/README.md'
    v='Hy-MT2 ailesi 21 Mayıs 2026 duyurusuyla 1.8B, 7B ve 30B-A3B olarak yayımlandı. İncelenen 1.8B hash: 9a341cd1b679d3efd23b46e847b01745a71ed792.'
    replace(106,'Tencent Hy-MT2 ve diğer çeviri adayları','Eski 1.5 yerine ayrı kartı okunan Hy-MT2 gösterildi. Diğer geliştiricilerin modelleri aynı sürüm ailesi sayılmadı.',[u],{
      'id':'tencent/Hy-MT2-1.8B','name':'Tencent Hy-MT2; Seed-X; NiuTrans LMT-60',
      'plain':'Tencent Hy-MT2, çeviri talimatlarını ve terim/bağlam koşullarını izlemeyi amaçlayan çok dilli çeviri ailesidir. Bu tur 1.8B kartı okundu. Seed-X ve NiuTrans ayrı ailelerdir; ayrıntılı incelemeleri açık.',
      'training':'Resmî kart çeviri talimatlarını izlemeyi ve IFMTBench sınavını anlatıyor. Okunan bölümlerden eğitim korpusu ve adım sayısı kesinleştirilmedi.',
      'version':v,'revision':'9a341cd1b679d3efd23b46e847b01745a71ed792',
      'try_it':'Hy-MT2 kartında Transformers, vLLM ve SGLang kullanım yolları var. Türkçe için aynı kaynak metin, terim listesi ve biçim kuralıyla denenebilir; bu oturumda çalıştırılmadı.',
      'independent':'Önceki sürümdeki Japonca–Vietnamca kullanıcı sorunu güncel Hy-MT2 sonucu sayılmadı. Bu sürüm için kontrollü bağımsız Türkçe kullanım testi doğrulanmadı.',
      'members':[{'name':'tencent/Hy-MT2-1.8B','url':'https://huggingface.co/tencent/Hy-MT2-1.8B','status':'Güncel README ve API okundu.'},{'name':'Hy-MT2 büyük varyantlar; Seed-X; NiuTrans LMT-60','url':None,'status':'Ayrı kart ve sürüm incelemeleri açık.'}],
      'sources':[source(u,'Tencent Hy-MT2 resmî çeviri kartı'),source('https://huggingface.co/api/models/tencent/Hy-MT2-1.8B','Hy-MT2 sürüm metadata kaydı')],
      'channels':channels([u],v,'Güncel Hy-MT2 kartı ve API okundu; önceki sürümün kullanıcı şikâyeti buraya aktarılmadı.')})

if 173 in cards:
    r=cards[173];u='https://ai.google.dev/gemma/docs/embeddinggemma/model_card_2?hl=en';b='https://huggingface.co/BAAI/bge-m3/raw/main/README.md'
    v='BGE-M3: 5617a9f61b028005a4858fdac845db406aefb181. EmbeddingGemma 2: 914f7f89142e33e77833254d9c9b90c3cef7303b, dosya değişimi 6 Ekim 2026; eğitim tarihi sayılmadı.'
    cc=channels([b,u],v,'BGE-M3 kartı ve güncel EmbeddingGemma 2 resmî kartı okundu.')
    cc[1]={'channel':'community','status':'checked','note':'BGE-M3 için ortam ve bütünleştirme yorumları okundu. Önceki Gemma üyelerinin yorumları EmbeddingGemma 2 kalitesi sayılmadı. Türkçe kontrollü test yok.','urls':['https://www.reddit.com/r/OpenWebUI/comments/1na4b5n']}
    replace(173,'BGE-M3 ve EmbeddingGemma 2','Eski EmbeddingGemma 300M yerine resmî kartı ve API kaydı okunan EmbeddingGemma 2 gösterildi.',[u],{
      'name':'BAAI/BGE-M3 ve Google EmbeddingGemma 2',
      'plain':'Bunlar belge bulmak için içerikleri sayısal temsillere çevirir. BGE-M3 çok dilli metin aramasını; EmbeddingGemma 2 metin, görsel, video ve ses için ortak temsil uzayını hedefler. Aynı Türkçe görevde ayrı ölçülmeliler.',
      'claims':r['claims']+[{'text':'EmbeddingGemma 2, toplam 740 milyon parametreli modüler yapıyla dört içerik türünü 768 boyutlu ortak uzaya eşliyor.','evidence':'Google resmî kartının mimari/işlev tarifi; Türkçe üstünlük sonucu değil.','source':u}],
      'version':v,'revision':None,
      'try_it':'BGE-M3 model kartındaki arama örnekleri ve EmbeddingGemma 2 resmî dokümanındaki cihazda kullanım yolu incelenebilir. Aynı sorgu/belge kümesiyle denenmeli; bu oturumda kurulmadı veya çalıştırılmadı.',
      'independent':'OpenWebUI başlığında BGE-M3 için çalışan bütünleştirme bildiriliyor; bu ortam deneyimi doğruluk ölçümü değildir. Önceki Gemma üyesine ait yorumlar yeni EmbeddingGemma 2 için kullanılmadı.',
      'members':[x for x in r['members'] if '300m' not in x['name'].lower()],
      'sources':[source(b,'BGE-M3 resmî kartı')]+[x for x in r['sources'] if 'embeddinggemma-2' in x['url'] or 'model_card_2' in x['url'] or 'reddit.com' in x['url']],
      'channels':cc})

if 123 in cards:
    r=cards[123]
    replace(123,'Erk-32B / Erk-14B · v2','Güncel ana dalın v2 olduğu doğrulandı; eski v1 etiketleri etkin başlık yerine araştırma arşivinde kaldı.',[s['url'] for s in r['sources'] if 'huggingface.co' in s['url']],{'name':'Erk-32B / Erk-14B · v2'})

if 157 in cards:
    replace(157,'LEXPERA LEXI · 2.0','Geliştiricinin güncel ürün sayfasındaki 2.0 adı gösterildi; ürün sürümü model ağırlığı sayılmadı.',['https://www.lexpera.com.tr/lexi-yapay-zeka'],{'name':'LEXPERA LEXI 2.0'})

(ROOT/'arastirma/eleme-kararlari.json').write_text(json.dumps(selection,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'excluded':len(selection['excluded']),'updated_groups':len(selection['replacements'])}))
