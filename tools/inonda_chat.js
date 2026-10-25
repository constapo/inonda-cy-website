/* INONDA LTD shared guided chatbot. Local answers; no API, tracking or auto-send. */
(function(){'use strict';
const DATA=__INONDA_CHAT_COPY__,UI=__INONDA_CHAT_UI__;
const phones={Irina:'35794091616',Constantin:'35794091613'};
const normal=q=>String(q).toLowerCase().normalize('NFD').replace(/\p{Diacritic}/gu,'');
function categories(question){const q=normal(question);return Object.entries({
 cleaning:/clean|καθαρ|уборк|прибиран|curat|ניקיון/,
 renovation:/renovat|refurb|paint|kitchen|bathroom|tiling|ανακαιν|βαψ|κουζιν|μπανι|renovar|zugrav|bucatar|baie|ремонт|שיפו/,
 handyman:/handyman|small fix|μικρο|мелк|дрібн|reparatii mici|תיקונים קטנים/,
 maintenance:/maintenance|maintain|συντηρ|обслуж|intretin|תחזוק/,
 landscaping:/garden|landscap|κηπ|сад|gradin|גינון/,
 management:/manage|tenant|landlord|διαχειρ|управл|administr|ניהול/
}).filter(([,pattern])=>pattern.test(q)).map(([id])=>id);}
function classify(question){const q=normal(question);
 if(/websites?|inonda\.(site|org|homes)|ιστοτοπ|са[йи]т|אתר|site.uri/.test(q))return 'network';
 if(/contact|whats|viber|phone|call|email|book|quote|appointment|irina|constantin|επικοιν|τηλεφ|κλεισ|προσφορ|связ|контакт|звон|осмотр|огляд|oferta|program|התקשר|קשר|טלפון|לתאם|תיאום/.test(q))return 'contact';
 if(/\bvat\b|\btax\b|φπα|\btva\b|ндс|пдв|מע.מ/.test(q))return 'vat';
 if(/warrant|guarant|εγγυ|гарант|garant|אחריות|he490415/.test(q))return 'warranty';
 if(/price|cost|budget|much|pay|τιμη|κοστο|ποσο|προυπολογ|pret|стоим|бюджет|варт|ціна|кошту|скільки|תקציב|מחיר|עלות|buget/.test(q))return 'budget';
 if(/plumb|electri|emergen|urgent|licensed|υδραυλ|ηλεκτρ|επειγ|електр|электр|сантех|urgent|instalat|חשמל|אינסטל/.test(q))return 'specialist';
 if(/where|area|location|cyprus|nicosia|limassol|address|strovolos|larnaca|paphos|που|κυπρ|λευκωσ|λεμεσ|адрес|кипр|кіпр|unde|adresa|locati|איפה|כתובת|קפריס/.test(q))return 'area';
 if(/commercial|office|shop|residential|villa|apartment|επαγγελμα|κατοικ|γραφει|коммерч|жило|комерц|житло|rezident|birou|מגורים|מסחר/.test(q)&&!categories(q).length)return 'property';
 const selected=categories(q);if(selected.length>1)return 'combination';if(selected.length)return selected[0]==='handyman'?'maintenance':selected[0];
 if(/save|download|print|compare|αποθηκε|ληψη|εκτυπ|скачат|завантаж|зберег|descarc|salv|הורד|שמיר/.test(q))return 'save';
 if(/month|weekly|recurr|frequency|μηνι|εβδομαδ|συχνοτ|месяц|місяц|lunar|frecvent|חודש|תדיר/.test(q))return 'frequency';
 return 'start';
}
function requestText(request,lang){const u=UI[lang]||UI.en;return [u[37]+' · INONDA LTD',u[20]+': '+(request.service||''),u[21]+': '+(request.property||''),u[22]+': '+(request.area||''),u[23]+': '+(request.details||'')].join('\n');}
function draftUrl(person,text){if(!Object.hasOwn(phones,person))return null;return 'https://wa.me/'+phones[person]+'?text='+encodeURIComponent(text);}
if(typeof module!=='undefined'&&module.exports)module.exports={classify,categories,requestText,draftUrl,data:DATA,ui:UI};
if(typeof document==='undefined')return;
let lang=Object.hasOwn(UI,document.documentElement.lang)?document.documentElement.lang:'en';
let request=null,stage=null,started=false;
const site=document.body.dataset.inondaSite||'homes',isHome=site==='homes';
const u=()=>UI[lang],d=()=>DATA[lang];
function el(tag,cls,text){const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=text;return e;}
const toggle=el('button','inonda-chat-toggle');toggle.id='inonda-chat-toggle';toggle.type='button';toggle.setAttribute('aria-controls','inonda-chat-panel');toggle.setAttribute('aria-expanded','false');toggle.dataset.noI18n='';
const mark=el('img');mark.src=isHome?'./inonda-logo.png':'/assets/logo-68.png';mark.alt='';mark.width=36;mark.height=29;toggle.append(mark,el('span','inonda-chat-toggle-label',u()[0]));
const panel=el('dialog','inonda-chat-panel');panel.id='inonda-chat-panel';panel.dataset.noI18n='';panel.setAttribute('aria-labelledby','inonda-chat-title');
const head=el('div','inonda-chat-head'),titles=el('div'),title=el('h2','',u()[1]);title.id='inonda-chat-title';const subtitle=el('p','',u()[2]),close=el('button','inonda-chat-close',u()[3]);close.type='button';titles.append(title,subtitle);head.append(titles,close);
const log=el('div','inonda-chat-log');log.id='inonda-chat-log';log.setAttribute('role','log');log.setAttribute('aria-live','polite');log.setAttribute('aria-relevant','additions');
const quick=el('div','inonda-chat-quick'),form=el('form','inonda-chat-form'),inputLabel=el('label','inonda-chat-sr',u()[9]),input=el('input');input.id='inonda-chat-input';inputLabel.htmlFor=input.id;input.maxLength=600;input.autocomplete='off';input.placeholder=u()[9];const send=el('button','inonda-chat-send',u()[10]);send.type='submit';form.append(inputLabel,input,send);const privacy=el('p','inonda-chat-privacy',u()[11]);panel.append(head,log,quick,form,privacy);document.body.append(toggle,panel);
function scrollLog(){requestAnimationFrame(()=>{log.scrollTop=log.scrollHeight;});}
function bubble(text,visitor=false){const row=el('div','inonda-chat-message'+(visitor?' inonda-chat-visitor':''));row.append(el('small','',visitor?u()[36]:u()[1]),el('p','',text));log.append(row);scrollLog();return row;}
function button(parent,label,action){const b=el('button','',label);b.type='button';b.addEventListener('click',action);parent.append(b);return b;}
function link(parent,label,href,channel){const a=el('a','',label);a.href=href;if(/^https:\/\/wa\.me/.test(href)){a.target='_blank';a.rel='noopener noreferrer';}if(channel){a.dataset.inondaChannel=channel;const icon=el('img','inonda-channel-icon');icon.src=(isHome?'./':'/assets/')+channel+'-official.svg';icon.alt='';icon.width=24;icon.height=24;a.prepend(icon);}parent.append(a);return a;}
function estimateUrl(ids=[]){const query=new URLSearchParams({lang});if(ids.length)query.set('services',ids.join(','));return 'https://www.inonda.homes/?'+query+'#property';}
function websiteUrl(key){return key==='management'?'https://www.inonda.site/'+lang+'/property-management-services/':'https://www.inonda.org/'+lang+'/services/';}
function openEstimate(ids=[]){if(isHome){if(ids.length)document.dispatchEvent(new CustomEvent('inonda:add-services',{detail:{services:ids}}));panel.close();document.querySelector(ids.length?'#services':'#property')?.scrollIntoView({behavior:'smooth'});}else location.href=estimateUrl(ids);}
function choices(items){quick.replaceChildren();items.forEach(([label,fn])=>button(quick,label,fn));}
function homeChoices(){choices([[u()[5],explore],[u()[6],begin],[u()[7],()=>openEstimate()],[u()[8],contacts]]);}
function actionLinks(row,ids=[]){const actions=el('div','inonda-chat-actions');link(actions,ids.length===1&&ids[0]==='management'?u()[30]:u()[29],websiteUrl(ids.length===1&&ids[0]==='management'?'management':'services'));if(isHome)button(actions,u()[7],()=>openEstimate(ids));else link(actions,u()[7],estimateUrl(ids));button(actions,u()[6],begin);row.append(actions);scrollLog();}
function contacts(){const row=bubble(d().faq.contact.text),actions=el('div','inonda-chat-actions');for(const [person,number]of Object.entries(phones)){link(actions,'WhatsApp · '+person,'https://wa.me/'+number,'whatsapp');link(actions,'Viber · '+person,'viber://chat?number=%2B'+number,'viber');}link(actions,'inonda2026@outlook.com','mailto:inonda2026@outlook.com');row.append(actions);homeChoices();scrollLog();}
function explore(){bubble(u()[12]);choices([...Object.entries(d().services).map(([id,label])=>[label,()=>{bubble(label,true);answer(id==='handyman'?'maintenance':id,id); }]),[u()[13],()=>answer('specialist')],[u()[6],begin]]);}
function answer(topic,question=''){
 const ids=categories(question||topic);
 if(topic==='specialist'){const row=bubble(u()[31]);actionLinks(row);homeChoices();return;}
 if(topic==='combination'){const row=bubble(u()[28]+' '+ids.map(id=>d().services[id]).join(' + '));actionLinks(row,ids);homeChoices();return;}
 if(topic==='contact'){contacts();return;}
 if(topic==='budget'){
  if(isHome){const detail={question:question||'What is my current budget?',answer:null};document.dispatchEvent(new CustomEvent('inonda:guide-question',{detail}));const row=bubble(detail.answer?.text||u()[33]);actionLinks(row);}
  else{const row=bubble(u()[33]);actionLinks(row,ids);}homeChoices();return;
 }
 const info=d().faq[topic]||d().faq.start,row=bubble(info.text);
 actionLinks(row,ids);homeChoices();
}
function begin(){request={service:'',property:'',area:'',details:''};stage='service';promptStage();input.focus();}
function promptStage(){
 const cancel=[u()[27],()=>{request=null;stage=null;homeChoices();bubble(u()[4]);}];
 if(stage==='service'){bubble(u()[12]);choices([...Object.entries(d().services).map(([id,label])=>[label,()=>receive(label,id)]),[u()[13],()=>receive(u()[13],'other')],cancel]);}
 if(stage==='property'){bubble(u()[14]);choices([[u()[15],()=>receive(u()[15])],[u()[16],()=>receive(u()[16])],cancel]);}
 if(stage==='area'){bubble(u()[17]);choices([...Object.entries(d().locations).map(([key,label])=>[label,()=>receive(label)]),cancel]);}
 if(stage==='details'){bubble(u()[18]);choices([cancel]);}
}
function receive(value,id){const text=String(value).trim().slice(0,600);if(!text)return;bubble(text,true);
 if(stage==='service'){request.service=text;request.serviceId=id||'other';stage='property';promptStage();}
 else if(stage==='property'){request.property=text.slice(0,100);stage='area';promptStage();}
 else if(stage==='area'){request.area=text.slice(0,100);stage='details';promptStage();}
 else if(stage==='details'){request.details=text;stage=null;summary();}
 input.value='';
}
function summary(){const text=requestText(request,lang),row=bubble(u()[19]);row.append(el('pre','inonda-chat-request',text));const actions=el('div','inonda-chat-actions');
 for(const person of Object.keys(phones))link(actions,u()[24]+' · '+person,draftUrl(person,text),'whatsapp');
 link(actions,u()[25],'mailto:inonda2026@outlook.com?subject='+encodeURIComponent(u()[37])+'&body='+encodeURIComponent(text));
 for(const [person,number]of Object.entries(phones))link(actions,'Viber · '+person,'viber://chat?number=%2B'+number,'viber');
 row.append(actions,el('p','inonda-chat-draft-note',u()[38]));choices([[u()[26],begin],[u()[7],()=>openEstimate(request.serviceId==='other'?[]:[request.serviceId])],[u()[8],contacts]]);scrollLog();
}
function ask(text){const question=text.trim();if(!question)return;if(stage){receive(question);return;}bubble(question,true);answer(classify(question),question);input.value='';}
function update(){lang=Object.hasOwn(UI,document.documentElement.lang)?document.documentElement.lang:'en';toggle.querySelector('span').textContent=u()[0];title.textContent=u()[1];subtitle.textContent=u()[2];close.textContent=u()[3];inputLabel.textContent=u()[9];input.placeholder=u()[9];send.textContent=u()[10];privacy.textContent=u()[11];panel.dir=lang==='he'?'rtl':'ltr';if(stage)promptStage();else homeChoices();}
toggle.addEventListener('click',()=>{if(panel.open){panel.close();return;}panel.show();toggle.setAttribute('aria-expanded','true');if(!started){bubble(u()[4]);started=true;}if(stage)promptStage();else homeChoices();input.focus();});
close.addEventListener('click',()=>panel.close());panel.addEventListener('close',()=>{toggle.setAttribute('aria-expanded','false');toggle.focus();});panel.addEventListener('keydown',event=>{if(event.key==='Escape')panel.close();});form.addEventListener('submit',event=>{event.preventDefault();ask(input.value);});document.addEventListener('inonda:language',update);update();
})();
