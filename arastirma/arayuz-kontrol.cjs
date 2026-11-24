// Gerçek tarayıcı değildir: üretilen JS'nin veri/filtre akışını kontrol eder.
const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const base=path.resolve(__dirname,'..'),html=fs.readFileSync(path.join(base,'sayfalar/TURKCE-MODEL-LABORATUVARI.html'),'utf8');
const elements=new Map();
function element(id){if(!elements.has(id))elements.set(id,{textContent:'',innerHTML:'',value:id==='status'?'all':id==='task'?'asr':'',disabled:false,events:{},options:[],addEventListener(e,fn){this.events[e]=fn},add(option){if(this.options.length===0)this.value=option.value;this.options.push(option)}});return elements.get(id)}
for(const m of html.matchAll(/<script id="([^"]+)" type="application\/json">([\s\S]*?)<\/script>/g))element(m[1]).textContent=m[2];
const context=vm.createContext({document:{getElementById:element},Option:function(text,value){this.text=text;this.value=value},Map,Set,URL,console});
const scripts=[...html.matchAll(/<script(?: [^>]*)?>([\s\S]*?)<\/script>/g)];vm.runInContext(scripts.at(-1)[1],context);
let checks=0;function test(name,fn){fn();checks++;console.log('PASS '+name)}
const select=(id,value)=>{element(id).value=value;element(id).events[id==='query'?'input':'change']()};
const selection=JSON.parse(element('selection-data').textContent);
test('Özgün kaynak ve etkin kayıt sayıları ayrı',()=>{assert.equal(JSON.parse(element('catalog-data').textContent).length,190);assert(element('count').textContent.startsWith((190-selection.excluded.length)+' '))});
test('ilk sayfada 15 kayıt',()=>assert.equal((element('entries').innerHTML.match(/class="entry"/g)||[]).length,15));
test('sayfa değişimi durum metnini değiştirir',()=>{element('next').events.click();assert(element('page').textContent.startsWith('Sayfa 2 /'))});
test('WHISPER araması sonuç bulur',()=>{select('query','WHISPER');assert(!element('count').textContent.startsWith('0 '))});
test('Whisper ile WHISPER aynı',()=>{const x=element('count').textContent;select('query','Whisper');assert.equal(element('count').textContent,x)});
test('boş sonuç açıklaması görünür',()=>{select('query','olmayan-model-9e0784');assert(element('entries').innerHTML.includes('Eşleşen kayıt yok'))});
select('query','');
test('model filtresi model olmayanları çıkarır',()=>{select('status','models');assert(!element('entries').innerHTML.includes('Tür: Veri kümesi'))});
test('kimlik belirsiz filtresi çalışır',()=>{select('status','identity');assert(!element('count').textContent.startsWith('190 '));assert(element('entries').innerHTML.includes('Kimlik / erişim belirsiz'))});
test('araştırma açığı filtresi',()=>{select('status','limited');assert(!element('count').textContent.startsWith('0 '))});
select('status','all');
test('kategori filtresi TTS',()=>{select('category','TTS');assert(element('count').textContent.startsWith('19 '))});
test('seslendirme deney planı',()=>{select('task','tts');assert(element('plan').innerHTML.includes('Yazı → ses'));assert(element('plan').innerHTML.includes('yalnız deney taslağı'))});
test('açıklama alanlarında kaynak kanalları var',()=>{select('category','');select('query','Kumru');assert(element('entries').innerHTML.includes('Hangi kanallara bakıldı?'))});
test('Kaldırılmış Piper sesleri görünmez, DFKI korunur',()=>{select('query','DFKI');assert(element('entries').innerHTML.includes('Piper Türkçe sesleri'));assert(!element('entries').innerHTML.includes('Fahrettin'));assert(!element('entries').innerHTML.includes('Fettah'))});
test('Durdurulan Antalia yerine güncel Mini görünür',()=>{select('query','Antalia-2 Mini');assert(element('entries').innerHTML.includes('1.0.1'));assert(!element('entries').innerHTML.includes('Antalia1'));assert(!element('entries').innerHTML.includes('Antalia-1'))});
test('Yorum eksikliği erişilebilir modeli elemez',()=>{select('query','RsGoksel_ITU_Mainframe');assert(!element('count').textContent.startsWith('0 '))});
test('Eski Google morphology yerine TRmorph kolu görünür',()=>{select('query','TRmorph');assert(element('entries').innerHTML.includes('xfst/foma'));assert(!element('entries').innerHTML.includes('google-research/turkish-morphology'))});
console.log(JSON.stringify({checks,scope:'Node VM üzerinde veri ve olay akışı; tarayıcı, görsel veya ekran okuyucu kabulü değildir.'}));
