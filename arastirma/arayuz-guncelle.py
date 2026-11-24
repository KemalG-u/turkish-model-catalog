"""Araştırma kapsamını görünür kılan kaynak kanalları ve filtreleri ekler."""
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'sayfalar/turkce-model-laboratuvari.template.html'
s=p.read_text(encoding='utf-8')
s=s.replace('İlk araştırma turu · 23 Ekim 2026','Katalog araştırması · 23 Ekim 2026')
s=s.replace('<option value="all">Tüm kayıtlar</option><option value="reviewed" selected>İlk kaynak kartı eklenenler</option><option value="pending">İlk kaynak kartı bekleyenler</option>','<option value="all" selected>Tüm kayıtlar</option><option value="models">Model ve model aileleri</option><option value="limited">Araştırma açığı olanlar</option><option value="identity">Kimliği / erişimi çözülemeyenler</option><option value="nonmodel">Veri, araç, makale ve sınavlar</option>')
s=s.replace('function match(c){for(const r of researched){if(c.url && c.url.replace(/\\/$/,\'\').toLowerCase()===(\'https://huggingface.co/\'+r.id).toLowerCase())return r}return null}',"const recordIds=new Map(catalog.map((c,i)=>[c,i+1]));\nfunction match(c){return researched.find(r=>r.record_id===recordIds.get(c))||null}")
start=s.index('function detail(c,r)');end=s.index('\nfunction render()',start)
s=s[:start]+r'''const kindNames={model:'Model',model_family:'Model ailesi / birleşik kayıt',product:'Ürün / hizmet',dataset:'Veri kümesi',benchmark:'Sınav / değerlendirme',paper:'Makale / yöntem',tool:'Araç / kaynak listesi',unknown:'Kimliği belirsiz'};
const channelNames={developer:'Geliştiricinin açıklamaları',community:'Kullanıcılar ve topluluk',social_video:'Blog, sosyal paylaşım ve video',version:'Sürüm ve devam çalışmaları'};
const channelStates={checked:'Kontrol edildi',searched_not_found:'Arandı; doğrulanabilir içerik bulunamadı',inaccessible:'Erişilemedi',not_applicable:'Bu kayıt için doğrudan uygulanmıyor',not_searched:'Bu kanalda inceleme yapılmadı'};
function badge(r){if(!r)return 'Araştırma bekliyor';if(r.research_status==='identity_unresolved')return 'Kimlik / erişim belirsiz';if(r.research_status==='limited')return 'Kaynak tarandı · Açık sorular var';if(r.research_status==='non_model')return 'Kaynak tarandı · Model değil';return 'Kaynak tarandı · Deney yapılmadı'}
function detail(c,r){
 if(!r)return `<p><strong>Araştırma bekliyor.</strong> Bu kayda yeni kaynak kartı henüz eklenmedi.</p>${raw(c)}`;
 const rev=revisions.find(v=>v.id?.toLowerCase()===r.id.toLowerCase());
 const channels=(r.channels||[]).map(x=>`<li><strong>${esc(channelNames[x.channel]||x.channel)}: ${esc(channelStates[x.status]||x.status)}</strong><p>${esc(x.note)}</p>${(x.urls||[]).map((u,i)=>`<a href="${esc(url(u))}" target="_blank" rel="noopener noreferrer">Kanal kaynağı ${i+1}</a>`).join(' · ')}</li>`).join('');
 const members=(r.members||[]).map(x=>`<li>${x.url?`<a href="${esc(url(x.url))}" target="_blank" rel="noopener noreferrer">${esc(x.name)}</a>`:esc(x.name)}<p class="small">${esc(x.status||'Üye araştırması açık')}</p></li>`).join('');
 return `<p>${esc(r.plain)}</p><p class="small">Katalog kaydı #${r.record_id}. Tür: ${esc(kindNames[r.kind]||'İlk kaynak kartı')}. İncelenen kimlik: ${esc(r.name)}.</p>
 ${r.research_status==='identity_unresolved'?'<div class="notice"><strong>Bu kaydın kimliği veya erişimi çözülemedi.</strong> Eski notları doğrulanmış bilgi sayma.</div>':''}
 <h4>Geliştiricisi ne iddia ediyor?</h4>${(r.claims||[]).length?(r.claims||[]).map(x=>`<div class="claim"><p><strong>${esc(x.text)}</strong></p><p>${esc(x.evidence)}</p>${x.source?`<a href="${esc(url(x.source))}" target="_blank" rel="noopener noreferrer">İddianın kaynağı</a>`:''}</div>`).join(''):'<p>Bu turda kaynağı okunarak doğrulanabilen açık bir iddia çıkarılamadı.</p>'}
 ${field(r.kind==='dataset'||r.kind==='benchmark'?'Nasıl oluşturulmuş?':'Nasıl geliştirilmiş?',r.training)}${field('Sürüm ve takip çalışmaları',r.version)}
 ${r.revision||rev?`<details class="raw"><summary>Teknik sürüm kimliğini gör</summary><p class="small">${esc(r.revision||rev.sha)}${rev?.lastModified?' · '+esc(rev.lastModified):''}. Depodaki değişiklik tarihi yeni eğitim anlamına gelmez.</p></details>`:''}
 ${field('Nasıl deneyebilirim?',r.try_it)}${r.demo_url?`<p><a href="${esc(url(r.demo_url))}" target="_blank" rel="noopener noreferrer">Geliştiricinin deneme sayfasını aç</a> <span class="small">(Bu çalışmada denenmedi.)</span></p>`:''}
 ${field('Başkaları ne diyor?',r.independent)}${members?`<details class="raw"><summary>Bu kayıttaki üyeler ve araştırma kapsamı</summary><ul>${members}</ul><p class="small">Bir üyenin sonucu diğer üyelerin sonucu değildir. Listelenen kapsam dışında bütün ailenin araştırıldığı varsayılmaz.</p></details>`:''}
 ${channels?`<h4>Hangi kanallara bakıldı?</h4><ul class="sources">${channels}</ul>`:''}<h4>Açık kalan sorular</h4><ul>${(r.unknowns||[]).map(x=>`<li>${esc(readable(x))}</li>`).join('')}</ul>
 <h4>Kaynaklar ve kontrol tarihleri</h4><ul class="sources">${(r.sources||[]).map(x=>`<li><a href="${esc(url(x.url))}" target="_blank" rel="noopener noreferrer">${esc(x.title)}</a><div class="source-meta">${esc(x.type)} · ${esc({read:'İlgili metin / metadata okundu',inaccessible:'İçeriğe erişilemedi',discovery_only:'Yalnız keşif izi'}[x.status]||'İlk tur kaynağı')} · Kaynak tarihi: ${esc(x.date||'belirtilmemiş')} · Kontrol: ${esc(x.checked_at||'2026-10-23')}</div></li>`).join('')}</ul>
 <p class="small">Bu bir kaynak araştırmasıdır. Kendi model deneyimiz yok. Aramada bulunmayan bilgiye yok denmez; kapalı eğitim veya bütün internetteki son sürüm garanti edilmez.</p>${raw(c)}`;
}
''' + s[end:]
start=s.index('function render()');end=s.index('\nfor(const el of',start)
s=s[:start]+r'''function render(){
 const q=searchKey(query.value.trim());
 const rows=catalog.filter(c=>{const r=match(c);const st=status.value;const model=['model','model_family'].includes(r?.kind);const open=r?.research_status==='limited'||r?.research_status==='identity_unresolved'||(r?.channels||[]).some(x=>['inaccessible','not_searched'].includes(x.status));return (!category.value||c.tur===category.value)&&(st==='all'||(st==='models'?model:st==='limited'?open:st==='identity'?r?.research_status==='identity_unresolved':st==='nonmodel'?!model&&!!r:false))&&(!q||searchKey(JSON.stringify([c,r])).includes(q))});
 const pages=Math.ceil(rows.length/size);page=Math.min(page,Math.max(0,pages-1));
 document.getElementById('count').textContent=`${rows.length} katalog kaydı. Bunlar tek tek model sayısı değildir.`;
 document.getElementById('entries').innerHTML=rows.length?rows.slice(page*size,(page+1)*size).map(c=>{const r=match(c);return `<details class="entry"><summary><div><span class="badge ${!r||['limited','identity_unresolved'].includes(r.research_status)?'old':''}">${esc(badge(r))}</span><h3>${esc(c.ad)}</h3>${r?`<p>${esc(r.plain)}</p>`:''}${r&&r.name!==c.ad?`<p class="small">Bu kartın kapsamı: ${esc(r.name)}. Diğer aile üyelerinin durumu ayrıntıda.</p>`:''}<span class="small">${esc(names[c.tur]||c.tur)} · ${esc(r?.creator||c.yapan)} · ${esc(kindNames[r?.kind]||'Araştırılacak')}</span></div></summary><div class="detail">${detail(c,r)}</div></details>`}).join(''):'<p class="empty">Eşleşen kayıt yok. Başka bir sözcük dene veya filtreleri genişlet.</p>';
 document.getElementById('page').textContent=`Sayfa ${pages?page+1:0} / ${pages}`;document.getElementById('prev').disabled=page===0;document.getElementById('next').disabled=page+1>=pages;
}
''' + s[end:]
s=s.replace('`${catalog.filter(c=>match(c)).length} kayda ilk kaynak kartı eklendi.`','`${catalog.filter(c=>match(c)).length} kayda kaynak araştırması eklendi. Açık sorular ve erişim sınırları kartlarda görünür.`')
s=s.replace('<strong>İlk tur sınırı:</strong> Aşağıdaki kartlar örnek başlangıç araştırmasıdır. Bütün kanalların veya 190 kaydın derin araştırmasının tamamlandığı anlamına gelmez. Genel bir kategori kazananı seçilmedi.','<strong>Araştırmanın sınırı:</strong> Her kaydın geliştirici, topluluk, sosyal/video ve sürüm kanalları ayrı gösterilir. Erişilemeyen ve incelenmeyen noktalar saklanmaz. Bir kartın bulunması bütün aile üyelerinin ve tüm internetin araştırıldığı anlamına gelmez. Genel bir kategori kazananı seçilmedi.')
s=s.replace('Kaynak kontrolü: 23 Ekim 2026.','Kaynak kontrolü: 23 Ekim 2026. Sayfadaki araştırma, modelin kendi deneyimizde başarılı olduğunu göstermez.')
p.write_text(s,encoding='utf-8')
print('Arayüzde kapsam, tür, sürüm ve kanal görünürlüğü güncellendi.')
